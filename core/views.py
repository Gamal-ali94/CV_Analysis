from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CandidateForm, PromptForm
from .models import Candidate
from .ocr import extract_text_from_file
import json
import openai
import os
from .openai_services import parse_resume_with_llm

# Create your views here.
def upload_cv(request):
    if request.method == 'POST':
        form = CandidateForm(request.POST, request.FILES)
        if form.is_valid():
            candidate = form.save()
            file_path = candidate.uploaded_file.path
            extracted_text = extract_text_from_file(file_path)
            try:
                candidate_data = json.loads(parse_resume_with_llm(extracted_text))
            except json.JSONDecodeError:
                messages.error(request, "We encountered an issue parsing your CV. Please try again.")
                candidate.delete()
                return redirect('upload_cv')
            except Exception as e:
                messages.error(request, f"An unexpected error occurred: {str(e)}")
                candidate.delete()
                return redirect('upload_cv')
            
            candidate.personal_info = candidate_data["personal_info"]
            candidate.education = candidate_data["education"]
            candidate.work_experience = candidate_data["work_experience"]
            candidate.skills = candidate_data["skills"]
            candidate.projects = candidate_data["projects"]
            candidate.certificates = candidate_data["certificates"]
            candidate.save()
            return redirect('candidate_view', pk=candidate.id)
    else:
        form = CandidateForm()

    return render(request, 'core/upload.html', {'form': form})

def candidate_view(request, pk):
    candidate = Candidate.objects.get(pk=pk)
    return render(request, 'core/candidate.html', {'candidate': candidate})


 
def handle_response(request):
    messages = request.session.get('messages', [])
    if request.method == 'POST':
            form = PromptForm(request.POST)
            if form.is_valid():
                candidate_data = Candidate.objects.values("personal_info", "education", "work_experience", "skills", "projects", "certificates")
                prompt = form.cleaned_data['prompt']
                messages.append({"role": "user", "content": f"Use this prompt {prompt} and an answer from {candidate_data}"})
                response = openai.chat.completions.create(
                    model="gpt-4o-2024-08-06",
                    messages=messages
                )
                final_response = response.choices[0].message.content
                messages.append({"role":final_response})
                request.session['final_response'] = final_response
                request.session['messages'] = messages
                return redirect('chat_response')
    else:
        form = PromptForm()
        final_response = request.sessions.get('final_response', "")

    return render(request, 'core/handle_response.html', {'form': form, 'final_response':final_response})