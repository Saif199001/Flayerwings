from rest_framework import generics

from .models import Tool
from .serializers import ToolSerializer


class ToolListView(generics.ListAPIView):
    serializer_class = ToolSerializer

    def get_queryset(self):
        return Tool.objects.filter(is_active=True)


class ToolDetailView(generics.RetrieveAPIView):
    serializer_class = ToolSerializer
    lookup_field = "slug"

    def get_queryset(self):
        return Tool.objects.filter(is_active=True)
