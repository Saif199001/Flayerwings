from django.urls import path

from .views import (
    ToolDocumentDetailView,
    ToolDocumentListCreateView,
    ToolDocumentPDFView,
    ToolEventCreateView,
    ToolListView,
    ToolStatsView,
    ToolTemplateListView,
)

urlpatterns = [
    path("", ToolListView.as_view(), name="tool-list"),
    path("templates/<slug:slug>/", ToolTemplateListView.as_view(), name="tool-templates"),
    path("documents/", ToolDocumentListCreateView.as_view(), name="document-list-create"),
    path("documents/<uuid:pk>/", ToolDocumentDetailView.as_view(), name="document-detail"),
    path("documents/<uuid:pk>/pdf/", ToolDocumentPDFView.as_view(), name="document-pdf"),
    path("events/", ToolEventCreateView.as_view(), name="event-create"),
    path("stats/<slug:slug>/", ToolStatsView.as_view(), name="tool-stats"),
]
