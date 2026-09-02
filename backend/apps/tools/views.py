from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView

from .models import ToolDefinition, ToolDocument, ToolEvent, ToolTemplate
from .serializers import ToolDefinitionSerializer, ToolDocumentSerializer, ToolEventSerializer, ToolTemplateSerializer
from .services import document_pdf_response


class ToolListView(generics.ListAPIView):
    queryset = ToolDefinition.objects.filter(active=True)
    serializer_class = ToolDefinitionSerializer


class ToolTemplateListView(generics.ListAPIView):
    serializer_class = ToolTemplateSerializer

    def get_queryset(self):
        return ToolTemplate.objects.filter(tool__slug=self.kwargs["slug"], active=True).select_related("tool")


class ToolDocumentListCreateView(generics.ListCreateAPIView):
    serializer_class = ToolDocumentSerializer
    throttle_scope = "tool_document"
    throttle_classes = [ScopedRateThrottle]

    def get_queryset(self):
        qs = ToolDocument.objects.select_related("tool", "template")
        if self.request.user.is_authenticated:
            return qs.filter(user=self.request.user)
        visitor_id = self.request.query_params.get("visitor_id", "")
        return qs.filter(visitor_id=visitor_id) if visitor_id else qs.none()

    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save(user=user)


class ToolDocumentDetailView(generics.RetrieveAPIView):
    serializer_class = ToolDocumentSerializer
    throttle_scope = "tool_document"
    throttle_classes = [ScopedRateThrottle]

    def get_queryset(self):
        qs = ToolDocument.objects.select_related("tool", "template")
        if self.request.user.is_authenticated:
            return qs.filter(user=self.request.user)
        visitor_id = self.request.query_params.get("visitor_id", "")
        return qs.filter(visitor_id=visitor_id) if visitor_id else qs.none()


class ToolDocumentPDFView(APIView):
    throttle_scope = "tool_pdf"
    throttle_classes = [ScopedRateThrottle]

    def get(self, request, pk):
        qs = ToolDocument.objects.select_related("tool", "template")
        if request.user.is_authenticated:
            qs = qs.filter(user=request.user)
        else:
            visitor_id = request.query_params.get("visitor_id", "")
            qs = qs.filter(visitor_id=visitor_id) if visitor_id else qs.none()
        document = get_object_or_404(qs, pk=pk)
        return document_pdf_response(document)


class ToolEventCreateView(generics.CreateAPIView):
    serializer_class = ToolEventSerializer
    throttle_scope = "tool_event"
    throttle_classes = [ScopedRateThrottle]

    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save(user=user)


class ToolStatsView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_scope = "tool_stats"
    throttle_classes = [ScopedRateThrottle]

    def get(self, request, slug):
        tool = get_object_or_404(ToolDefinition, slug=slug, active=True)
        events = ToolEvent.objects.filter(tool=tool).values("event_type").annotate(count=Count("id"))
        return Response({
            "tool": tool.slug,
            "events": list(events),
            "documents": ToolDocument.objects.filter(tool=tool).count(),
        })
