from django.urls import path
from .views import *
from django.contrib.sitemaps.views import sitemap

sitemaps = {
    'static': StaticViewSitemap,
}

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('', create_request, name='create_request'),
    path('request_history/', request_history, name='request_history'),
    path('logout/', logout_view, name='logout'),
    path('robots.txt', robots_txt, name='robots_txt'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
]
   