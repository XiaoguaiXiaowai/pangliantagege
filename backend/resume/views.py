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

        # context 传入 request，使序列化器可按 ?lang= 返回对应语言的内容
        ctx = {'request': request}
        return Response({
            'basic_info': BasicInfoSerializer(basic_info, context=ctx).data if basic_info else None,
            'skills': SkillSerializer(skills, many=True, context=ctx).data,
            'tech_stack': TechStackSerializer(tech_stack, many=True, context=ctx).data,
            'experiences': ExperienceSerializer(experiences, many=True, context=ctx).data,
            'projects': ProjectSerializer(projects, many=True, context=ctx).data,
            'educations': EducationSerializer(educations, many=True, context=ctx).data,
            'certificates': CertificateSerializer(certificates, many=True, context=ctx).data,
        })
