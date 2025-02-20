import openai
from django.conf import settings

openai.api_key = settings.OPENAI_KEY


def parse_resume_with_llm(raw_text: str):
    """
    Parse resume text using OpenAI's Large Language Model.

    This function takes raw text extracted from a resume and uses OpenAI's GPT model
    to structure it into predefined categories according to a specific schema.

    Args:
        raw_text (str): The raw text extracted from the resume document.

    Returns:
        str: A JSON string containing structured resume data with the following sections:
            - personal_info: Basic information like name, email, phone, address
            - education: List of educational qualifications
            - work_experience: List of work experiences with details
            - skills: List of technical and soft skills
            - projects: List of projects with descriptions
            - certificates: List of certifications

    Raises:
        openai.error.OpenAIError: If there's an issue with the OpenAI API call
        json.JSONDecodeError: If the response cannot be parsed as valid JSON
    """

    system_message = {
        "role": "system",
        "content": (
            "You are a CV/Resume parser. You will receive the text from a CV and your task "
            "is to extract the following information:"
            "1. Personal Info"
            "2. Education"
            "3. Work Experience"
            "4. Skills"
            "5. Projects"
            "6. Certifications"
            "You must return only valid JSON with these exact top-level keys:"
            "personal_info, education, work_experience, skills, projects, certificates."
            "Do not include any additional commentary. Output must be valid JSON only."
        ),
    }

    user_message = {"role": "user", "content": raw_text}

    schema = {
        "type": "json_schema",
        "json_schema": {
            "name": "cv_resume_parser",
            "schema": {
                "type": "object",
                "properties": {
                    "personal_info": {
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "Full name of the individual",
                            },
                            "email": {
                                "type": "string",
                                "description": "Email address of the individual",
                            },
                            "phone": {
                                "type": "string",
                                "description": "Phone number of the individual",
                            },
                            "address": {
                                "type": "string",
                                "description": "Postal address of the individual",
                            },
                        },
                        "required": ["name", "email", "phone", "address"],
                        "additionalProperties": False,
                    },
                    "education": {
                        "type": "array",
                        "description": "List of educational qualifications",
                        "items": {
                            "type": "object",
                            "properties": {
                                "degree": {
                                    "type": "string",
                                    "description": "Degree obtained",
                                },
                                "institution": {
                                    "type": "string",
                                    "description": "Name of the educational institution",
                                },
                                "year": {
                                    "type": "string",
                                    "description": "Year of graduation",
                                },
                            },
                            "required": ["degree", "institution", "year"],
                            "additionalProperties": False,
                        },
                    },
                    "work_experience": {
                        "type": "array",
                        "description": "List of work experiences",
                        "items": {
                            "type": "object",
                            "properties": {
                                "job_title": {
                                    "type": "string",
                                    "description": "Title of the job held",
                                },
                                "company": {
                                    "type": "string",
                                    "description": "Company where the job was held",
                                },
                                "start_date": {
                                    "type": "string",
                                    "description": "Start date of employment",
                                },
                                "end_date": {
                                    "type": "string",
                                    "description": "End date of employment",
                                },
                                "responsibilities": {
                                    "type": "string",
                                    "description": "Key responsibilities held during the job",
                                },
                            },
                            "required": [
                                "job_title",
                                "company",
                                "start_date",
                                "end_date",
                                "responsibilities",
                            ],
                            "additionalProperties": False,
                        },
                    },
                    "skills": {
                        "type": "array",
                        "description": "List of skills possessed by the individual",
                        "items": {"type": "string"},
                    },
                    "projects": {
                        "type": "array",
                        "description": "List of projects undertaken by the individual",
                        "items": {
                            "type": "object",
                            "properties": {
                                "project_name": {
                                    "type": "string",
                                    "description": "Name of the project",
                                },
                                "description": {
                                    "type": "string",
                                    "description": "Brief description of the project",
                                },
                                "technologies": {
                                    "type": "string",
                                    "description": "Technologies used in the project",
                                },
                            },
                            "required": ["project_name", "description", "technologies"],
                            "additionalProperties": False,
                        },
                    },
                    "certificates": {
                        "type": "array",
                        "description": "List of certifications acquired by the individual",
                        "items": {
                            "type": "object",
                            "properties": {
                                "certificate_name": {
                                    "type": "string",
                                    "description": "Name of the certification",
                                },
                                "issued_by": {
                                    "type": "string",
                                    "description": "Name of the organization that issued the certification",
                                },
                                "year": {
                                    "type": "string",
                                    "description": "Year the certification was obtained",
                                },
                            },
                            "required": ["certificate_name", "issued_by", "year"],
                            "additionalProperties": False,
                        },
                    },
                },
                "required": [
                    "personal_info",
                    "education",
                    "work_experience",
                    "skills",
                    "projects",
                    "certificates",
                ],
                "additionalProperties": False,
            },
            "strict": True,
        },
    }

    response = openai.chat.completions.create(
        model="gpt-4o-2024-08-06",
        messages=[system_message, user_message],
        response_format=schema,
    )

    return response.choices[0].message.content
