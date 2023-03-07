from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from .models import Link
from .serializers import LinkSerializer, LinkCreateSerializer, LinkUpdateSerializer
from .filters import LinkModelFilter


class LinkViewSet(ModelViewSet):
    """
    CRUD for Link model.
    Prohibits updating the 'receivables' field via API.
    """
    queryset = Link.objects.all()
    filter_backends = (DjangoFilterBackend, )
    filterset_class = LinkModelFilter

    def get_serializer_class(self):
        if self.action == 'create':
            return LinkCreateSerializer
        elif self.action == 'update':
            return LinkUpdateSerializer
        else:
            return LinkSerializer
