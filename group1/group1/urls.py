from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from requirements.views import users
from requirements.views import home
from issue_tracker.viewsets import UserViewSet
from rest_framework.routers import DefaultRouter
from chat.views import index
from rest_framework.authtoken import views

router = DefaultRouter()
router.register(r'users', UserViewSet)


urlpatterns = patterns(
    '',
    url(r'^signin', users.signin),
    url(r'^signout', users.signout),
    url(r'^signup', users.signup),
    url(r'^requirements/', include('requirements.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', home.home_page),
    url(r'^communication/', index),
    url(r'^issue_tracker/', include('issue_tracker.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^api/', include(router.urls)),
    url(r'^api-token-auth/', views.obtain_auth_token)
)
