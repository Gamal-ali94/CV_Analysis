from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Candidate
from .forms import CandidateForm
import json
from unittest.mock import patch

# Create your tests here.

class UploadCVViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.upload_url = reverse('upload_cv')

    def test_get_upload_page(self):
        """Test that the upload page loads correctly"""
        response = self.client.get(self.upload_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/upload.html')
        self.assertIsInstance(response.context['form'], CandidateForm)

    def test_upload_cv_successful(self):
        """Test successful CV upload with valid form data"""
        # Create a mock PDF file
        mock_file = SimpleUploadedFile(
            "test_cv.pdf",
            b"file_content",
            content_type="application/pdf"
        )

        # Mock the extracted data
        mock_personal_info = {
            "name": "John Doe",
            "email": "john@example.com"
        }

        # Patch the text extraction and parsing functions
        with self.settings(MEDIA_ROOT='test_media/'), \
             patch('core.views.extract_text_from_file', return_value="some text"), \
             patch('core.views.parse_cv_text_with_schema', 
                   return_value=json.dumps({"personal_info": mock_personal_info})):

            # Submit the form with the test file
            response = self.client.post(self.upload_url, {
                'name': 'John Doe',
                'email': 'john@example.com',
                'uploaded_file': mock_file
            })

            # Check that a new candidate was created
            self.assertEqual(Candidate.objects.count(), 1)
            candidate = Candidate.objects.first()
            
            # Check that we were redirected to the candidate view
            self.assertRedirects(response, 
                               reverse('candidate_view', kwargs={'pk': candidate.id}))
            
            # Verify the personal info was saved correctly
            self.assertEqual(candidate.personal_info, mock_personal_info)

    def test_upload_cv_invalid_form(self):
        """Test CV upload with invalid form data"""
        response = self.client.post(self.upload_url, {})
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/upload.html')
        self.assertTrue(response.context['form'].errors)
        self.assertEqual(Candidate.objects.count(), 0)
