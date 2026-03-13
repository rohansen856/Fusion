from rest_framework import serializers

from applications.placement_cell.models import (Achievement, Course, Education,
                                                Experience, Has, Patent,
                                                Project, Publication, Skill,
                                                PlacementStatus, NotifyStudent,
                                                PlacementRecord, ChairmanVisit)

class SkillSerializer(serializers.ModelSerializer):

    class Meta:
        model = Skill
        fields = ('__all__')

class HasSerializer(serializers.ModelSerializer):
    skill_id = SkillSerializer()

    class Meta:
        model = Has
        fields = ('skill_id','skill_rating')

    def create(self, validated_data):
        skill = validated_data.pop('skill_id')
        skill_id, created = Skill.objects.get_or_create(**skill)
        try:
            has_obj = Has.objects.create(skill_id=skill_id,**validated_data)
        except:
            raise serializers.ValidationError({'skill': 'This skill is already present'})
        return has_obj

class EducationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Education
        fields = ('__all__')

class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ('__all__')

class ExperienceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Experience
        fields = ('__all__')

class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ('__all__')

class AchievementSerializer(serializers.ModelSerializer):

    class Meta:
        model = Achievement
        fields = ('__all__')

class PublicationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Publication
        fields = ('__all__')

class PatentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Patent
        fields = ('__all__')

class NotifyStudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = NotifyStudent
        fields = ('__all__')

class PlacementStatusSerializer(serializers.ModelSerializer):
    notify_id = NotifyStudentSerializer()

    class Meta:
        model = PlacementStatus
        fields = ('notify_id', 'invitation', 'placed', 'timestamp', 'no_of_days')


class PlacementRecordSerializer(serializers.ModelSerializer):

    class Meta:
        model = PlacementRecord
        fields = ('id', 'placement_type', 'name', 'ctc', 'year', 'test_score', 'test_type')


class PlacementRecordCreateSerializer(serializers.Serializer):
    placement_type = serializers.ChoiceField(choices=PlacementRecord._meta.get_field('placement_type').choices)
    name = serializers.CharField(max_length=100)
    ctc = serializers.DecimalField(max_digits=5, decimal_places=2, required=False)
    year = serializers.IntegerField()
    test_score = serializers.IntegerField(required=False, allow_null=True)
    test_type = serializers.CharField(max_length=30, required=False, allow_blank=True)

    def validate_year(self, value):
        if value < 2000:
            raise serializers.ValidationError('Year must be >= 2000')
        return value

    def validate_ctc(self, value):
        if value < 0:
            raise serializers.ValidationError('CTC cannot be negative')
        return value


class ChairmanVisitSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChairmanVisit
        fields = ('id', 'company_name', 'location', 'visiting_date', 'description', 'timestamp')


class ChairmanVisitCreateSerializer(serializers.Serializer):
    company_name = serializers.CharField(max_length=100)
    location = serializers.CharField(max_length=100)
    visiting_date = serializers.DateField()
    description = serializers.CharField(required=False, allow_blank=True)

    def validate_company_name(self, value):
        if not value.strip():
            raise serializers.ValidationError('Company name is required')
        return value.strip()


class PlacementStatisticsSerializer(serializers.Serializer):
    year = serializers.IntegerField()
    total_records = serializers.IntegerField()
    avg_ctc = serializers.DecimalField(max_digits=5, decimal_places=2, allow_null=True)
