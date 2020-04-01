from django.contrib import admin
from django.db.models import Count

from core.models import Image, Video
from user_profile.models import Profile


# class FollowersFilter(admin.SimpleListFilter):
#     title = 'Followers amount'
#     parameter_name = 'followers_amount'
#
#     def lookups(self, request, model_admin):
#         return (
#             (9, 'LESS THAN 10'),
#             (10, 'MORE THAN 10'),
#             (1000, 'MORE THAN 1000'),
#             (100000, 'MORE THAN 100000'),
#         )
#
#     def queryset(self, request, queryset):
#         value = self.value()
#         try:
#             value = int(value)
#         except TypeError:
#             value = ''
#
#         if value == 9:
#             return queryset.filter(followers_amount__lt=value)
#         elif value == 10 or value == 1000 or value == 100000:
#             return queryset.filter(followers_amount__gt=value)
#         else:
#             return queryset


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['username', 'date_joined', 'following_amount', 'images_amount', 'videos_amount']
    list_filter = ['date_joined']

    def following_amount(self, profile):
        return profile.followers_amount

    following_amount.admin_order_field = 'followers_amount'

    def get_queryset(self, request):
        qs = (Profile.objects.annotate(followers_amount=Count('followed_by')))
        return qs

    def images_amount(self, profile):
        return Image.objects.filter(user=profile).count()

    def videos_amount(self, profile):
        return Video.objects.filter(user=profile).count()
