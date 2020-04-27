from rest_framework import serializers
from .models import Contact
from .tasks import mail_admins_task


class ContactSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(allow_blank=True, required=False)

    def send_admin_mail(self, data):
        name = data['name']
        message = data['message']
        mail_admins_task.send(
            subject=f'New message from {name}',
            message=message
        )

    def validate(self, data):
        if data['phone']:
            raise serializers.ValidationError('Rejected')
        return data

    def create(self, validated_data):
        validated_data.pop('phone')
        self.send_admin_mail(validated_data)
        return super().create(validated_data)

    class Meta:
        model = Contact
        fields = '__all__'
