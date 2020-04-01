from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path

from core.views import ProfileDetailView, FeedView, LikeView, CommentView

app_name = 'core'
urlpatterns = [
    path('', FeedView.as_view(), name='feed'),
    path('profile/<username>', ProfileDetailView.as_view(), name='to_profile'),
    path('like/', LikeView.as_view(), name='like'),
    path('comment/', CommentView.as_view(), name='comment'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
