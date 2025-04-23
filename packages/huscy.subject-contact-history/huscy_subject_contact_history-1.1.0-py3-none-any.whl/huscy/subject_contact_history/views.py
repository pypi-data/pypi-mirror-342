from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from huscy.subject_contact_history.serializer import ContactHistorySerializer
from huscy.subject_contact_history.services import get_contact_history
from huscy.subjects.models import Subject


class ContactHistoryViewSet(CreateModelMixin, ListModelMixin, GenericViewSet):
    lookup_url_kwarg = 'subject_pk'
    permission_classes = (IsAuthenticated, )
    queryset = Subject.objects.all()
    serializer_class = ContactHistorySerializer

    def perform_create(self, serializer):
        serializer.save(subject=self.get_object())

    def list(self, request, *args, **kwargs):
        subject = self.get_object()
        contact_history_items = get_contact_history(subject)
        serializer = self.get_serializer(contact_history_items, many=True)
        return Response(serializer.data)
