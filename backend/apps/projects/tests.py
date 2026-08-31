from django.test import TestCase
from django.urls import reverse

from .models import Project


class ProjectApiTests(TestCase):
    def setUp(self):
        Project.objects.create(
            title="Flayer Wings SaaS",
            slug="flayer-wings-saas",
            project_type=Project.ProjectType.PRODUCT,
            status=Project.Status.IN_PROGRESS,
            short_description="Upcoming SaaS product.",
            featured=True,
            published=True,
        )
        Project.objects.create(
            title="Unpublished Project",
            slug="unpublished-project",
            project_type=Project.ProjectType.CLIENT,
            short_description="Private project.",
            published=False,
        )

    def test_list_returns_only_published_projects(self):
        response = self.client.get(reverse("project-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["slug"], "flayer-wings-saas")

    def test_detail_returns_published_project(self):
        response = self.client.get(reverse("project-detail", kwargs={"slug": "flayer-wings-saas"}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["project_type"], "product")

    def test_detail_hides_unpublished_project(self):
        response = self.client.get(reverse("project-detail", kwargs={"slug": "unpublished-project"}))
        self.assertEqual(response.status_code, 404)
