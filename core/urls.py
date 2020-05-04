from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path

from core.views import ProfileDetailView, FeedView, LikeView, CommentView, FollowersView, FollowView, ImageDetailView, \
    VideoDetailView, AddViewsToVideo, HashTagPostListView, PlacePostListView, ImageCommentsView, AddImageView

app_name = 'core'
urlpatterns = [
    path('', FeedView.as_view(), name='feed'),
    path('profile/<username>', ProfileDetailView.as_view(), name='to_profile'),
    path('profile/<username>/followers', FollowersView.as_view(), name='to_profile_followers'),
    path('like/', LikeView.as_view(), name='like'),
    path('follow/', FollowView.as_view(), name='follow'),
    path('comment/', CommentView.as_view(), name='comment'),
    path('image/<int:pk>', ImageDetailView.as_view(), name='to_image'),
    path('video/<int:pk>', VideoDetailView.as_view(), name='to_video'),
    path('add_view/', AddViewsToVideo.as_view(), name='add_view'),
    path('hashtag/<hashtag>', HashTagPostListView.as_view(), name='hashtag'),
    path('place/<place_slug>', PlacePostListView.as_view(), name='place'),
    path('image/<int:pk>/comments', ImageCommentsView.as_view(), name='image_comments'),
    path('add/image', AddImageView.as_view(), name='add_image'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
