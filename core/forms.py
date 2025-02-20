import os

from django import forms

from .models import Candidate


class CandidateForm(forms.ModelForm):
    """
    A Django ModelForm for handling CV uploads to the Candidate model.

    This form enforces:
      - File extension must be either .pdf or .docx.
      - File size must be under 5MB.
    If these checks fail, a ValidationError is raised.

    Fields:
        uploaded_file (FileField): The CV file to be uploaded.
    """

    class Meta:
        model = Candidate
        fields = ["uploaded_file"]

    def clean_uploaded_file(self):
        file = self.cleaned_data["uploaded_file"]
        if file:
            extension = os.path.splitext(file.name)[1].lower()
            if extension not in [".pdf", ".docx"]:
                raise forms.ValidationError("Only PDF and DOCX files are supported.")

            max_size = 5
            if file.size > max_size * 1024 * 1024:
                raise forms.ValidationError(
                    f"File size should be less than {max_size} MB."
                )

        return file


class PromptForm(forms.Form):
    """
    A simple Django Form for capturing a user prompt (chat input).

    Fields:
        prompt (CharField): The text input for a chat query, displayed in a Textarea widget.
    """

    prompt = forms.CharField(label="Prompt", widget=forms.Textarea)
