from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import BasicInfo, Skill, Experience, Project, Education
from .serializers import (
    BasicInfoSerializer, SkillSerializer, ExperienceSerializer,
    ProjectSerializer, EducationSerializer
)

class ResumeViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing all resume data.
    """
    permission_classes = []  # Allow public access for now

    def list(self, request):
        basic_info = BasicInfo.objects.first()
        skills = Skill.objects.all()
        experiences = Experience.objects.all()
        projects = Project.objects.all()
        educations = Education.objects.all()

        return Response({
            'basic_info': BasicInfoSerializer(basic_info).data if basic_info else None,
            'skills': SkillSerializer(skills, many=True).data,
            'experiences': ExperienceSerializer(experiences, many=True).data,
            'projects': ProjectSerializer(projects, many=True).data,
            'educations': EducationSerializer(educations, many=True).data,
        })
