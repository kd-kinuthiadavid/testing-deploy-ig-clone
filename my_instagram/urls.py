from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

from my_instagram import views

urlpatterns=[
    url(r'^$', views.all_images, name='welcome'),
    url(r'^current_user_profile/(?P<profile_id>\d+)', views.my_profile, name='profile'),
    url(r'^explore_more/', views.explore, name='my_explore'),
    url(r'^new/image$', views.new_image, name='new-image'),
    url(r'^new/profile$', views.new_profile, name='new-profile'),
    url(r'follow/(?P<id>\d+)', views.follow, name='follow'),
    url(r'all_profiles/', views.all_profiles, name='all_profiles'),
    url(r'single_profile/(?P<id>\d+)', views.single_profile, name='single_profile'),
    url(r'comment/(?P<image_id>\d+)', views.comment, name='comment'),
    url(r'comment_per-image/(?P<id>\d+)', views.comment_per_image, name='comment_per_image'),
    url(r'^search/', views.search_results, name='search_results'),

]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
