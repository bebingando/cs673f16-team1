from django.conf import settings
from django.conf.urls import include
from django.conf.urls import patterns
from django.conf.urls.static import static
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles.views import serve
from django.contrib import admin
import views as it_views
import viewsets as it_viewsets
from rest_framework.routers import DefaultRouter

admin.autodiscover()

# Routers provide an easy way of automatically determining the URL conf.
router = DefaultRouter()
router.register(r'users', it_viewsets.UserViewSet, base_name='users')
router.register(r'issues', it_viewsets.IssueViewSet, base_name='issues')
router.register(r'issue', it_viewsets.IssueViewSetRO, base_name='issue')
router.register(r'comments', it_viewsets.CommentViewSet, base_name='comments')

router.register(r'status', it_viewsets.IssueStatusViewSet, base_name='status')
router.register(r'priority', it_viewsets.IssuePriorityViewSet, base_name='priority')
router.register(r'ModifyMultipleIssueFields', it_viewsets.EditIssueMultipleFieldsViewSet, base_name='ModifyMultipleFields')

urlpatterns = patterns(
    '',
    url(r'^$', login_required(it_views.AssigneeListIssuesView.as_view()), name='issue_index'),

    # static files path
    url(r'^%s(?P<path>.*)$' % settings.STATIC_URL.lstrip('/'), serve, {'show_indexes': True, 'insecure': False}),

    # Admin site setup.
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),

    # Rest framework
    url(r'^api/', include(router.urls)),

    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    url(r'^issue/create/$', login_required(it_views.CreateIssue.as_view()), name='create_issue'),
    url(r'^issue/assigned/$', login_required(it_views.AssigneeListIssuesView.as_view()), name='assigned_issues'),
    url(r'^issue/reported/$', login_required(it_views.ReporterListIssuesView.as_view()), name='reported_issues'),
    url(r'^issue/closed/$', login_required(it_views.ClosedListIssuesView.as_view()), name='closed_issues'),
    url(r'^issue/verified/$', login_required(it_views.VerifiedListIssuesView.as_view()), name='verified_issues'),
    url(r'^issue/multi/$', login_required(it_views.MultipleIssues.as_view()), name='multi_issue'),
    url(r'^issue/create/$', login_required(it_views.CreateIssue.as_view()), name='create_issue'),
    # For the uninitiated, pk is the primary key, which in our case is the bug id.
    url(r'^issue/view/(?P<pk>\d+)/$', login_required(it_views.ViewIssue.as_view()), name='view_issue'),
    url(r'^issue/edit/(?P<pk>\d+)/$', login_required(it_views.EditIssue.as_view()), name='edit_issue'),
    url(r'^issue/search/$', login_required(it_views.SearchIssues.as_view()), name='search'),

    #for interaction with issue comments via api:
    url(r'^Comments/$', it_views.CommentList.as_view(),name='comment-list'),
    url(r'^Comments/(?P<pk>[0-9]+)/$', it_views.CommentDetail.as_view(), name='comment-detail'),

    url(r'^issue/status/(?P<pk>\d+)/$', login_required(it_views.EditStatus.as_view()), name='issues_status'),
    url(r'^issue/priority/(?P<pk>\d+)/$', login_required(it_views.EditPriority.as_view()), name='issues_priority'),
    url(r'^issue/EditIssueMultipleFields/(?P<pk>\d+)/$', login_required(it_views.EditIssueMultipleFields.as_view()), name='EditIssueMultipleFields')
)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL )

