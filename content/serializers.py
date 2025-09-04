from rest_framework import serializers
from .models import LiveSession, Video, Syllabus, Module
#from assignment.serializers import AssignmentMiniSerializer
from .modules import ModuleMiniSerializer


class LiveSessionSerializer(serializers.ModelSerializer):
    module = ModuleMiniSerializer(read_only=True)
    module_id = serializers.PrimaryKeyRelatedField(queryset=Module.objects.all(), source='module', write_only=True)
    class Meta:
        model = LiveSession
        fields = '__all__'

class VideoSerializer(serializers.ModelSerializer):
    module = ModuleMiniSerializer(read_only=True)
    module_id = serializers.PrimaryKeyRelatedField(queryset=Module.objects.all(), source='module', write_only=True)
    class Meta:
        model = Video
        fields = '__all__'

class VideoMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'title', 'duration']

class SyllabusWithVideosSerializer(serializers.ModelSerializer):
    videos = VideoMiniSerializer(many=True, read_only=True)

    class Meta:
        model = Syllabus
        fields = ['id', 'title', 'videos']

class SyllabusWithContentSerializer(serializers.ModelSerializer):
    videos = VideoMiniSerializer(many=True, read_only=True)
    #assignments = AssignmentMiniSerializer(many=True, read_only=True)

    class Meta:
        model = Syllabus
        fields = ['id', 'title', 'videos', 'assignments']