from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import BasicInfo, Skill, TechStack, Experience, Project, Education, Certificate
from .serializers import (
    BasicInfoSerializer, SkillSerializer, TechStackSerializer, 
    ExperienceSerializer, ProjectSerializer, EducationSerializer, CertificateSerializer
)

class ResumeViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing all resume data.
    """
    permission_classes = []  # Allow public access for now

    def list(self, request):
        basic_info = BasicInfo.objects.first()
        skills = Skill.objects.all()
        tech_stack = TechStack.objects.all()
        experiences = Experience.objects.all()
        projects = Project.objects.all()
        educations = Education.objects.all()
        certificates = Certificate.objects.all()

        return Response({
            'basic_info': BasicInfoSerializer(basic_info).data if basic_info else None,
            'skills': SkillSerializer(skills, many=True).data,
            'tech_stack': TechStackSerializer(tech_stack, many=True).data,
            'experiences': ExperienceSerializer(experiences, many=True).data,
            'projects': ProjectSerializer(projects, many=True).data,
            'educations': EducationSerializer(educations, many=True).data,
            'certificates': CertificateSerializer(certificates, many=True).data,
        })
