from rest_framework import serializers
from .models import Module

class ModuleMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ['id', 'title']