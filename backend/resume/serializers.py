from rest_framework import serializers
from i18n_utils import LocalizedModelSerializerMixin
from .models import BasicInfo, Skill, TechStack, Experience, Project, Education, Certificate

class BasicInfoSerializer(LocalizedModelSerializerMixin, serializers.ModelSerializer):
    localized_fields = (
        'title', 'location', 'summary',
        'summary_experience', 'summary_skills', 'summary_management',
    )

    class Meta:
        model = BasicInfo
        fields = '__all__'

class SkillSerializer(LocalizedModelSerializerMixin, serializers.ModelSerializer):
    localized_fields = ('category',)

    class Meta:
        model = Skill
        fields = '__all__'

class TechStackSerializer(LocalizedModelSerializerMixin, serializers.ModelSerializer):
    localized_fields = ('major_category', 'minor_category')

    class Meta:
        model = TechStack
        fields = '__all__'

class ExperienceSerializer(LocalizedModelSerializerMixin, serializers.ModelSerializer):
    localized_fields = ('company', 'position', 'description')

    class Meta:
        model = Experience
        fields = '__all__'

class ProjectSerializer(LocalizedModelSerializerMixin, serializers.ModelSerializer):
    localized_fields = (
        'name', 'role', 'description',
        'bg_description', 'duty_description', 'solution_description', 'result_description',
    )

    class Meta:
        model = Project
        fields = '__all__'

class EducationSerializer(LocalizedModelSerializerMixin, serializers.ModelSerializer):
    localized_fields = ('school', 'degree', 'major')

    class Meta:
        model = Education
        fields = '__all__'

class CertificateSerializer(LocalizedModelSerializerMixin, serializers.ModelSerializer):
    localized_fields = ('name', 'issuer')

    class Meta:
        model = Certificate
        fields = '__all__'