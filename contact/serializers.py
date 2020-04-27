from rest_framework import serializers
from .models import Contact


class ContactSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(allow_blank=True, required=False)

    def validate(self, data):
        if data['phone']:
            raise serializers.ValidationError('Rejected')
        return data

    def create(self, validated_data):
        validated_data.pop('phone')
        return super().create(validated_data)

    class Meta:
        model = Contact
        fields = '__all__'
