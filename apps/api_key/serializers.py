from rest_framework import serializers
from .models import KaspiTokenAPI

class KaspiTokenAPISerializ(serializers.ModelSerializer):
    class Meta:
        model = KaspiTokenAPI
        fields = ('token_api', 'user')

class KaspiTokenAPICreateSerializ(serializers.ModelSerializer):
    class Meta:
        model = KaspiTokenAPI
        fields = ('token_api',)