from django.test import TestCase
from django.urls import reverse
from .models import Pages, PageReview
from .forms import PageReviewForm, HealthDataForm, IndexDataForm


class PagesModelTest(TestCase):
    def test_string_representation(self):
        page = Pages(title="Test Page")
        self.assertEqual(str(page), page.title)

    def test_pages_count(self):
        self.assertEqual(Pages.objects.count(), 0)
        Pages.objects.create(title="Test Page")
        self.assertEqual(Pages.objects.count(), 1)


class ViewsTest(TestCase):
    def setUp(self):
        self.page = Pages.objects.create(title="Test Page")
        self.review_url = reverse("add_review", kwargs={"pk": self.page.pk})

    def test_single_page_view(self):
        response = self.client.get(
            reverse("single_page_view", kwargs={"pk": self.page.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Page")

    def test_add_review_view(self):
        response = self.client.post(
            self.review_url, {"reviewer": "Test Reviewer", "content": "Test Content"}
        )
        self.assertEqual(
            response.status_code, 302
        )  # Redirects after successful review addition


class FormsTest(TestCase):
    def test_page_review_form(self):
        form_data = {"reviewer": "Test Reviewer", "content": "Test Content"}
        form = PageReviewForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_health_data_form(self):
        form_data = {
            "select_field": ["BE"],
            "select_field2": ["HLY_0"],
            "select_field3": "2022",
        }
        form = HealthDataForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_index_data_form(self):
        form_data = {"select_field": ["2022"], "select_field2": ["BE"]}
        form = IndexDataForm(data=form_data)
        self.assertTrue(form.is_valid())
