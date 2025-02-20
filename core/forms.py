import os
from django import forms
from .models import Candidate

class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ['uploaded_file']
    
    def clean_uploaded_file(self):
        file = self.cleaned_data['uploaded_file']
        if file:
            extension = os.path.splitext(file.name)[1].lower()
            if extension not in ['.pdf', '.docx']:
                raise forms.ValidationError("Only PDF and DOCX files are supported.")
            
            max_size = 5
            if file.size > max_size * 1024 * 1024:
                raise forms.ValidationError(f"File size should be less than {max_size} MB.")
            
        return file
    

class PromptForm(forms.Form):
    prompt = forms.CharField(label='Prompt', widget=forms.Textarea)