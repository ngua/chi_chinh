from rest_framework import serializers
from .models import Contact
from .tasks import mail_admins_task


class ContactSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(allow_blank=True, required=False)  # Honeypot

    def send_admin_mail(self, data):
        """
        Sends email to admin's defined in settings following successful POST
        to api endpoint. Calls dramatiq actor defined in tasks.py

        :param OrderedDict data: data from POST request
        """
        name = data['name']
        message = data['message']
        mail_admins_task.send(
            subject=f'New message from {name}',
            message=message
        )

    def validate(self, data):
        """
        Overrides parent method to checks serializer honeypot. If hidden
        `phone` field contains data or is missing from POST request, raises
        exception

        :param OrderedDict data: data from POST request
        :raise ValidationError:
        """
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
