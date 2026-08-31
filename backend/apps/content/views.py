from rest_framework import generics

from .models import SiteContent
from .serializers import SiteContentSerializer


class SiteContentListView(generics.ListAPIView):
    serializer_class = SiteContentSerializer

    def get_queryset(self):
        return SiteContent.objects.filter(is_published=True)


class SiteContentDetailView(generics.RetrieveAPIView):
    serializer_class = SiteContentSerializer
    lookup_field = "key"

    def get_queryset(self):
        return SiteContent.objects.filter(is_published=True)
