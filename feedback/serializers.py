from rest_framework import serializers

from feedback.models import Feedback


class FeedbackSerializer(serializers.ModelSerializer):
    name = serializers.CharField(label='имя отправителя', required=True)
    email = serializers.EmailField(label='контактный e-mail', required=True)
    message = serializers.CharField(required=True, label='сообщение')

    class Meta:
        model = Feedback
        fields = ('name', 'email', 'message', 'created_at')
