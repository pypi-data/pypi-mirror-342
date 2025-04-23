from django.conf import settings
from django.utils import timezone
from django.utils.timesince import timesince
from rest_framework import serializers

from huscy.subject_contact_history.models import ContactHistoryItem
from huscy.subject_contact_history.services import create_contact_history_item


class ContactHistorySerializer(serializers.ModelSerializer):
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())
    creator_username = serializers.SerializerMethodField(source='get_creator_username')
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    project_title = serializers.SerializerMethodField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    time_since = serializers.SerializerMethodField()

    class Meta:
        model = ContactHistoryItem
        fields = (
            'created_at',
            'creator',
            'creator_username',
            'project',
            'project_title',
            'status',
            'status_display',
            'time_since',
        )

    def create(self, validated_data):
        return create_contact_history_item(**validated_data)

    def get_creator_username(self, contact_history_item):
        return contact_history_item.creator.username

    def get_project_title(self, contact_history_item):
        project = contact_history_item.project
        return (project and project.title) or 'Deleted project'

    def get_time_since(self, contact_history_item):
        created_at = contact_history_item.created_at

        if settings.USE_TZ is False:
            created_at = timezone.make_naive(created_at)

        days_left = (timezone.now() - created_at).days
        depth = 1 if days_left < 400 else 2
        return timesince(contact_history_item.created_at, depth=depth)
