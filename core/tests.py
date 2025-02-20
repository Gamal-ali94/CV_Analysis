from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from .models import Candidate

# Remove rate limit middleware for testing
TEST_MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


class CandidateModelTests(TestCase):
    def setUp(self):
        """Set up test data"""
        self.candidate = Candidate.objects.create(
            personal_info={
                "name": "John Doe",
                "email": "john@example.com",
                "phone": "1234567890",
                "address": "123 Test St",
            },
            education=[
                {
                    "degree": "Bachelor's in Computer Science",
                    "institution": "Test University",
                    "year": "2020",
                }
            ],
            skills=["Python", "Django", "Testing"],
        )

    def test_candidate_str_method(self):
        """Test the string representation of Candidate model"""
        self.assertEqual(str(self.candidate), "Candidate: John Doe")

    def test_candidate_creation(self):
        """Test if candidate is created correctly"""
        self.assertTrue(isinstance(self.candidate, Candidate))
        self.assertEqual(self.candidate.personal_info["name"], "John Doe")
        self.assertEqual(len(self.candidate.skills), 3)


@override_settings(MIDDLEWARE=TEST_MIDDLEWARE)
class FormTests(TestCase):
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        # Create a minimal valid PDF file for testing
        self.test_file = SimpleUploadedFile(
            "test_cv.pdf",
            b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n2 0 obj<</Type/Pages/Count 1/Kids[3 0 R]>>endobj\n3 0 obj<</Type/Page/MediaBox[0 0 612 792]/Parent 2 0 R/Resources<<>>>>endobj\nxref\n0 4\n0000000000 65535 f\n0000000015 00000 n\n0000000061 00000 n\n0000000114 00000 n\ntrailer<</Size 4/Root 1 0 R>>\nstartxref\n190\n%%EOF\n",
            content_type="application/pdf",
        )

    def test_valid_file_upload(self):
        """Test uploading a valid PDF file"""
        response = self.client.post(
            reverse("upload_cv"), {"uploaded_file": self.test_file}
        )
        # Note: Since we can't fully test OCR and OpenAI in unit tests,
        # we'll just verify the form submission works
        self.assertIn(response.status_code, [200, 302])

    def test_invalid_file_type(self):
        """Test uploading an invalid file type"""
        invalid_file = SimpleUploadedFile(
            "test.txt", b"invalid file content", content_type="text/plain"
        )
        response = self.client.post(
            reverse("upload_cv"), {"uploaded_file": invalid_file}
        )
        self.assertEqual(
            response.status_code, 200
        )  # Should stay on same page with error


@override_settings(MIDDLEWARE=TEST_MIDDLEWARE)
class ViewTests(TestCase):
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.candidate = Candidate.objects.create(
            personal_info={
                "name": "Jane Smith",
                "email": "jane@example.com",
                "phone": "0987654321",
                "address": "456 Test Ave",
            }
        )

    def test_upload_cv_get(self):
        """Test GET request to upload_cv view"""
        response = self.client.get(reverse("upload_cv"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/upload.html")

    def test_candidate_view(self):
        """Test candidate detail view"""
        response = self.client.get(
            reverse("candidate_view", kwargs={"pk": self.candidate.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/candidate.html")


@override_settings(MIDDLEWARE=TEST_MIDDLEWARE)
class RateLimitMiddlewareTests(TestCase):
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        # Clear the cache before testing
        cache.clear()
        # Add the rate limit middleware back for this specific test
        with self.settings(
            MIDDLEWARE=TEST_MIDDLEWARE + ["core.middleware.RateLimitMiddleware"]
        ):
            self.test_client = Client()

    def test_rate_limit(self):
        """Test rate limiting"""
        # Make 11 requests (more than the limit of 10)
        with self.settings(
            MIDDLEWARE=TEST_MIDDLEWARE + ["core.middleware.RateLimitMiddleware"]
        ):
            for i in range(11):
                response = self.test_client.get(reverse("upload_cv"))
                if i < 10:
                    # The first 10 requests should pass
                    self.assertEqual(response.status_code, 200)
                else:
                    # The 11th request should be rate limited
                    self.assertEqual(response.status_code, 429)
