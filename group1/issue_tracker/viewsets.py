from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters
from rest_framework.response import Response
import models as it_models
import serializers


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class IssueViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows issues to be viewed or edited.
    """
    queryset = it_models.Issue.objects.all()
    serializer_class = serializers.IssueSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows comments to be viewed or edited.
    """
    queryset = it_models.IssueComment.objects.all()
    serializer_class = serializers.CommentSerializer


class IssueViewSetRO(viewsets.ReadOnlyModelViewSet):
    """
    Obtain a list of issues that meet a certain set of search criteria
    """
    queryset = it_models.Issue.objects.all()
    serializer_class = serializers.IssueSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = (
        'id',
        'title',
        'issue_type',
        'status',
        'priority',
        'project',
        'reporter',
        'assignee',
        'verifier'
    )

class IssueStatusViewSet(viewsets.ModelViewSet):
    queryset = it_models.Issue.objects.all()
    serializer_class = serializers.IssueSerializer

class IssuePriorityViewSet(viewsets.ModelViewSet):
    queryset = it_models.Issue.objects.all()
    serializer_class = serializers.IssueSerializer

class EditIssueMultipleFieldsViewSet(viewsets.ModelViewSet):
    queryset = it_models.Issue.objects.all()
    serializer_class = serializers.IssueSerializer
