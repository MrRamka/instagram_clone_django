import json
from functools import reduce
from itertools import chain

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, F
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import DetailView, ListView, TemplateView
from operator import or_, attrgetter

from core.comment_feed import FeedComment
from core.models import Image, Video, InstagramObject, ImageComment, VideoComment
from user_profile.models import Profile


class LikeView(LoginRequiredMixin, View):
    def post(self, request):
        if request.is_ajax():
            post_id = request.POST.get('post_id', None)
            post_type = request.POST.get('post_type', None)
            if post_type == 'Image':
                post = Image.objects.get(id=post_id)
            else:
                post = Video.objects.get(id=post_id)
            if request.user in post.likes.all():
                post.likes.remove(request.user)
            else:
                post.likes.add(request.user)
            data = {'likes': post.likes.all().count()}
            return HttpResponse(json.dumps(data), content_type='application/json')


class CommentView(LoginRequiredMixin, View):
    def post(self, request):
        if request.is_ajax():
            post_id = request.POST.get('post_id', None)
            post_type = request.POST.get('post_type', None)
            comment_body = request.POST.get('post_comment_body', None)
            status = 'OK'
            if post_type == 'Image':
                post = Image.objects.get(id=post_id)
                ImageComment.objects.create(user=request.user, image=post, comment_body=comment_body)
            else:
                post = Video.objects.get(id=post_id)
                VideoComment.objects.create(user=request.user, video=post, comment_body=comment_body)
            data = {'message': status}
            return HttpResponse(json.dumps(data), content_type='application/json')


class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'core/profile_detail.html'

    def get_object(self, **kwargs):
        return get_object_or_404(Profile, username=self.kwargs['username'])

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # followers amount
        followers_amount = Profile.objects.filter(follows=self.object).count()
        ctx['followers_amount'] = followers_amount
        # get images
        images = Image.objects.filter(user__username=self.object.username)
        ctx['user_images'] = images
        # get videos
        videos = Video.objects.filter(user__username=self.object.username)
        ctx['user_videos'] = videos
        return ctx


class FeedView(LoginRequiredMixin, TemplateView):
    template_name = 'core/feed.html'

    def get_comments(self, list_obj, obj_type, comments_amount=2):
        all_comments = []
        comment_amount = comments_amount
        for post in list_obj:
            comments = []
            post_comments = []
            # comments for each buddy
            if obj_type == Image:
                post_comments = ImageComment.objects.filter(image=post).order_by('-posted_on')[
                                :comment_amount + 1]
            elif obj_type == Video:
                post_comments = VideoComment.objects.filter(video=post).order_by('-posted_on')[
                                :comment_amount + 1]

            for post_comment in post_comments:
                # append comment
                comments.append(post_comment)
            # check for more comments
            if len(comments) == comment_amount + 1:
                all_comments.append(FeedComment(post, comments.copy()[:comment_amount], has_more=True))
            else:
                all_comments.append(FeedComment(post, comments.copy()[:comment_amount], has_more=False))
        return all_comments

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # get user
        user = self.request.user
        # get follows
        follows = user.follows.all()
        # get follows images limit 50
        feed_post_amount = 25
        images_buddies = Image.objects.prefetch_related('likes').filter(
            reduce(or_, [Q(user_id=c.id) for c in follows])).order_by('-posted_on')[:feed_post_amount]

        # get follows videos
        video_buddies = Video.objects.prefetch_related('likes').filter(
            reduce(or_, [Q(user_id=c.id) for c in follows])).order_by('-posted_on')[:feed_post_amount]

        all_posts = sorted(chain(images_buddies, video_buddies), key=attrgetter('posted_on'), reverse=True)
        ctx['posts'] = all_posts
        # get comments
        image_comment = self.get_comments(list_obj=images_buddies, obj_type=Image)
        video_comment = self.get_comments(list_obj=video_buddies, obj_type=Video)
        all_comments = image_comment + video_comment
        ctx['feed_comments'] = all_comments
        return ctx


class FollowersView(ListView):
    model = Profile
    template_name = 'core/followers.html'
    # simple pagination
    paginate_by = 5

    def get_object(self):
        """
        Get Profile object
        :return: Profile object
        """
        return get_object_or_404(Profile, username=self.kwargs['username'])

    def get_queryset(self):
        """
        Update queryset to show profile followers.
        :return followers queryset
        """
        queryset = Profile.objects.filter(follows=self.get_object())
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # put to context profile object
        user = self.get_object()
        ctx['profile'] = user
        return ctx


class FollowView(LoginRequiredMixin, View):
    """
    Method to handle follow ajax request
    """

    def post(self, request):
        status = 'OK'
        if request.is_ajax():
            username = request.POST.get('username', None)
            # session user
            curr_user = request.user
            # target user
            target_user = Profile.objects.get(username=username)
            # add to follow
            if target_user in curr_user.follows.all():
                curr_user.follows.remove(target_user)
                status = 'Removed'
            else:
                curr_user.follows.add(target_user)
                status = 'Added'
        else:
            status = 'BAD'
        data = {'status': status}
        return HttpResponse(json.dumps(data), content_type='application/json')


class ImageDetailView(DetailView):
    model = Image

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        # Add comments
        comment_amount = 10
        post_comments = ImageComment.objects.filter(image=self.object).order_by('-posted_on')[:comment_amount]
        ctx['post_comments'] = post_comments

        # add users subs
        subs_amount = Profile.objects.filter(follows=self.object.user).count()
        ctx['subs_amount'] = subs_amount

        return ctx


class VideoDetailView(DetailView):
    model = Video

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        # Add comments
        comment_amount = 10
        post_comments = VideoComment.objects.filter(video=self.object).order_by('-posted_on')[:comment_amount]
        ctx['post_comments'] = post_comments

        # add users subs
        subs_amount = Profile.objects.filter(follows=self.object.user).count()
        ctx['subs_amount'] = subs_amount

        return ctx


class AddViewsToVideo(View):
    """
        Method to handle video views ajax request
    """

    def post(self, request):
        if request.is_ajax():
            video_pk = request.POST.get('video_pk', None)

            video = Video.objects.get(id=video_pk)
            # Using F
            video.views = F('views') + 1
            video.save()

            all_views = Video.objects.get(id=video_pk).views
            # add to follow
            data = {'views': all_views}
            return HttpResponse(json.dumps(data), content_type='application/json')


class HashTagPostListView(FeedView):

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data(**kwargs)
        hashtag = self.kwargs['hashtag']
        # get follows images limit 50
        feed_post_amount = 25
        images = Image.objects.prefetch_related('likes').filter(
            hashtag__hashtag=hashtag).order_by('-posted_on')[:feed_post_amount]
        # get follows videos
        videos = Video.objects.prefetch_related('likes').filter(hashtag__hashtag=hashtag).order_by('-posted_on')[
                 :feed_post_amount]

        all_posts = sorted(chain(images, videos), key=attrgetter('posted_on'), reverse=True)
        ctx['posts'] = all_posts
        # get comments
        image_comment = self.get_comments(list_obj=images, obj_type=Image)
        video_comment = self.get_comments(list_obj=videos, obj_type=Video)
        all_comments = image_comment + video_comment
        ctx['feed_comments'] = all_comments
        return ctx


class PlacePostListView(FeedView):

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data(**kwargs)
        place_slug = self.kwargs['place_slug']
        # get follows images limit 50
        feed_post_amount = 25
        images = Image.objects.prefetch_related('likes').filter(
            place__place_slug=place_slug).order_by('-posted_on')[:feed_post_amount]
        # get follows videos
        videos = Video.objects.prefetch_related('likes').filter(
            place__place_slug=place_slug).order_by('-posted_on')[:feed_post_amount]

        all_posts = sorted(chain(images, videos), key=attrgetter('posted_on'), reverse=True)
        ctx['posts'] = all_posts
        # get comments
        image_comment = self.get_comments(list_obj=images, obj_type=Image)
        video_comment = self.get_comments(list_obj=videos, obj_type=Video)
        all_comments = image_comment + video_comment
        ctx['feed_comments'] = all_comments
        return ctx
