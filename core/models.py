from django.db import models


# Create your models here.
class Candidate(models.Model):
    """
    Model representing a candidate's parsed CV data.

    This model stores structured data extracted from uploaded CVs/resumes,
    including personal information, education history, work experience,
    skills, and other relevant details.

    Attributes:
        personal_info (JSONField): Stores basic candidate information like name,
            email, phone, and address.
        education (JSONField): List of educational qualifications including degree,
            institution, and graduation year.
        work_experience (JSONField): List of work experiences including job title,
            company, dates, and responsibilities.
        skills (JSONField): List of technical and soft skills.
        projects (JSONField): List of projects with names, descriptions, and technologies.
        certificates (JSONField): List of certifications with names and issuing organizations.
        uploaded_file (FileField): The original CV file that was uploaded.
        created_at (DateTimeField): Timestamp of when the record was created.
        updated_at (DateTimeField): Timestamp of when the record was last updated.
    """

    personal_info = models.JSONField(blank=True, null=True)
    education = models.JSONField(blank=True, null=True)
    work_experience = models.JSONField(blank=True, null=True)
    skills = models.JSONField(blank=True, null=True)
    projects = models.JSONField(blank=True, null=True)
    certificates = models.JSONField(blank=True, null=True)

    uploaded_file = models.FileField(upload_to="uploads/", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.personal_info and "name" in self.personal_info:
            return f"Candidate: {self.personal_info['name']}"
        return f"Candidate: {self.id}"
