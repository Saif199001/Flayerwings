from django.urls import path

from .views import SiteContentDetailView, SiteContentListView

urlpatterns = [
    path("", SiteContentListView.as_view(), name="content-list"),
    path("<slug:key>/", SiteContentDetailView.as_view(), name="content-detail"),
]
