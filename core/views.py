import json
from functools import reduce
from itertools import chain

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import DetailView, ListView
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

    def get_object(self):
        return get_object_or_404(Profile, username=self.kwargs['username'])

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        # get images
        images = Image.objects.filter(user__username=self.object.username)
        ctx['user_images'] = images
        # get videos
        videos = Video.objects.filter(user__username=self.object.username)
        ctx['user_videos'] = videos
        return ctx


class FeedView(LoginRequiredMixin, ListView):
    model = Image
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
