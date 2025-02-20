from django.db import models

# Create your models here.
class Candidate(models.Model):
    personal_info = models.JSONField(blank=True, null=True)
    education = models.JSONField(blank=True, null=True)
    work_experience = models.JSONField(blank=True, null=True)
    skills = models.JSONField(blank=True, null=True)
    projects = models.JSONField(blank=True, null=True)
    certificates = models.JSONField(blank=True, null=True)

    uploaded_file = models.FileField(upload_to='uploads/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.personal_info and "name" in self.personal_info:
            return f"Candidate: {self.personal_info['name']}"
        return f"Candidate: {self.id}"
    