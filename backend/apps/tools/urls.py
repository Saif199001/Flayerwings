from django.urls import path

from .generate_views import CaptionGenerateView, ContentIdeasView, SocialAuditView
from .views import ToolDetailView, ToolListView

urlpatterns = [
    path("", ToolListView.as_view(), name="tool-list"),
    path("<slug:slug>/", ToolDetailView.as_view(), name="tool-detail"),
    path("social-media-audit/generate/", SocialAuditView.as_view(), name="social-audit-generate"),
    path("caption-generator/generate/", CaptionGenerateView.as_view(), name="caption-generate"),
    path("content-ideas/generate/", ContentIdeasView.as_view(), name="content-ideas-generate"),
]
