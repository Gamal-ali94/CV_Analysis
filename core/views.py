import json

import openai
from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import CandidateForm, PromptForm
from .models import Candidate
from .ocr import extract_text_from_file
from .openai_services import parse_resume_with_llm


# Create your views here.
def upload_cv(request):
    """
    Handle the CV upload process.

    1. Renders a form (CandidateForm) to upload a CV (PDF or DOCX).
    2. On POST:
       - Validates the form.
       - Creates a Candidate model instance.
       - Attempts to retrieve the file path; if no file, raises an error.
       - Extracts text from the uploaded CV (OCR if needed).
       - Sends the text to OpenAI GPT to parse into structured data (JSON).
       - If parsing fails or an exception occurs, shows an error message and
         deletes the Candidate.
       - Otherwise, populates the Candidate fields from the parsed JSON and saves.
       - Redirects to candidate_view on success.
    """
    if request.method == "POST":
        form = CandidateForm(request.POST, request.FILES)
        if form.is_valid():
            candidate = form.save()
            try:
                file_path = candidate.uploaded_file.path
            except ValueError:
                messages.error(
                    request, "No file was provided, Upload a PDF or DOCX file."
                )
                candidate.delete()
                return redirect("upload_cv")
            extracted_text = extract_text_from_file(file_path)
            try:
                candidate_data = json.loads(parse_resume_with_llm(extracted_text))
            except json.JSONDecodeError:
                messages.error(
                    request,
                    "We encountered an issue parsing your CV. Please try again.",
                )
                candidate.delete()
                return redirect("upload_cv")
            except Exception as e:
                messages.error(request, f"An unexpected error occurred: {str(e)}")
                candidate.delete()
                return redirect("upload_cv")

            candidate.personal_info = candidate_data["personal_info"]
            candidate.education = candidate_data["education"]
            candidate.work_experience = candidate_data["work_experience"]
            candidate.skills = candidate_data["skills"]
            candidate.projects = candidate_data["projects"]
            candidate.certificates = candidate_data["certificates"]
            candidate.save()
            return redirect("candidate_view", pk=candidate.id)
    else:
        form = CandidateForm()

    return render(request, "core/upload.html", {"form": form})


def candidate_view(request, pk):
    """
    Display the parsed CV data for a single Candidate.
    """
    candidate = Candidate.objects.get(pk=pk)
    return render(request, "core/candidate.html", {"candidate": candidate})


def handle_response(request):
    """
    Provide a chatbot-like interface for querying candidate data.

    The conversation history is kept in session under "messages".
    - Each user prompt is appended as a 'user' role message.
    - The code then calls OpenAI (gpt-4o model) with these messages.
    - The assistant's reply is stored as "assistant" role, and
      saved to session under "final_response" for display.
    """
    messages = request.session.get("messages", [])
    if request.method == "POST":
        form = PromptForm(request.POST)
        if form.is_valid():
            candidate_data = Candidate.objects.values(
                "personal_info",
                "education",
                "work_experience",
                "skills",
                "projects",
                "certificates",
            )
            prompt = form.cleaned_data["prompt"]
            messages.append(
                {
                    "role": "user",
                    "content": f"You have access to this dataset of candidate resumes:{candidate_data}, THe user is asking: {prompt}, Answer only using the data above, or say 'not found' if unavaialble.",
                }
            )
            response = openai.chat.completions.create(
                model="gpt-4o-2024-08-06", messages=messages
            )
            final_response = response.choices[0].message.content
            messages.append({"role": "assistant", "content": final_response})
            request.session["final_response"] = final_response
            request.session["messages"] = messages
            return redirect("chat_prompt")
    else:
        form = PromptForm()
    final_response = request.session.get("final_response", "")

    return render(
        request,
        "core/handle_response.html",
        {"form": form, "final_response": final_response},
    )
