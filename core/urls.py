from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path

from core.views import ProfileDetailView, FeedView, LikeView, CommentView, FollowersView, FollowView, ImageDetailView

app_name = 'core'
urlpatterns = [
    path('', FeedView.as_view(), name='feed'),
    path('profile/<username>', ProfileDetailView.as_view(), name='to_profile'),
    path('profile/<username>/followers', FollowersView.as_view(), name='to_profile_followers'),
    path('like/', LikeView.as_view(), name='like'),
    path('follow/', FollowView.as_view(), name='follow'),
    path('comment/', CommentView.as_view(), name='comment'),
    path('image/<int:pk>', ImageDetailView.as_view(), name='to_image'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
