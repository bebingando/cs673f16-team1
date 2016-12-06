from issue_tracker.models import User, Issue, IssueComment
from requirements.models.project import Project
from rest_framework import routers, serializers, viewsets


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = (
            'url',
            'username',
            'email',
            'groups'
        )


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Project
        fields = (
            'title',
            'description',
            'last_updated'
        )


class IssueSerializer(serializers.HyperlinkedModelSerializer):
    reporter = UserSerializer()
    assignee = UserSerializer()
    verifier = UserSerializer()
    project = ProjectSerializer()

    class Meta:
        model = Issue
        fields = (
            'pk',
            'title',
            'description',
            'issue_type',
            'status',
            'priority',
            'project',
            'submitted_date',
            'modified_date',
            'closed_date',
            'reporter',
            'assignee',
            'verifier'
        )


class IssueCommentSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer()
    issue = IssueSerializer()

    class Meta:
        model = IssueComment
        fields = (
            'pk',
            'comment',
            'issue_id',
            'date',
            'poster',
            'is_comment'
        )

#This class is for serializing the comments alone. In which case we don't need to have an issue serialized.
class CommentSerializer(serializers.HyperlinkedModelSerializer):



    class Meta:
        model = IssueComment
        fields = (
            'pk',
            'comment',
            'issue_id',
            'date',
            'poster',
            'is_comment'
        )
