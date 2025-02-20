from django.contrib import admin
from .models import Candidate
# Register your models here.

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('id','created_at', 'updated_at')
    ordering = ["-created_at"]
