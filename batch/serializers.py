from rest_framework import serializers
from .models import Batch, BatchStudent
from accounts.models import CustomUser

class BatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = '__all__'

class BatchStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BatchStudent
        fields = '__all__'
