from rest_framework import generics

from .models import Lead
from .serializers import LeadCreateSerializer


class LeadCreateView(generics.CreateAPIView):
    queryset = Lead.objects.all()
    serializer_class = LeadCreateSerializer
