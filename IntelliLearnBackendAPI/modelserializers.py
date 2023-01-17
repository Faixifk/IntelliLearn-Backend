from rest_framework import serializers
from IntelliLearnBackendAPI.models import McqModel

class McqSerializer(serializers.ModelSerializer):

    class Meta:

        model = McqModel
        fields = '__all__'
