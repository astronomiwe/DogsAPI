from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from drf_yasg.utils import swagger_auto_schema

from rest_framework.response import Response
from rest_framework.views import APIView
from feedback.serializers import FeedbackSerializer

from config.settings import DEFAULT_FROM_EMAIL, RECIPIENTS_EMAIL, SENDGRID_API_KEY


class FeedbackView(APIView):
    @swagger_auto_schema(request_body=FeedbackSerializer, responses={201: ''})
    def post(self, request):
        """отправка сообщения через форму обратной связи"""
        serializer = FeedbackSerializer(data={'name': request.data.get('name'),
                                              'email': request.data.get('email'),
                                              'message': request.data.get('message')})
        serializer.is_valid(raise_exception=True)
        feedback = serializer.create(validated_data=serializer.validated_data)

        message = Mail(
            from_email=DEFAULT_FROM_EMAIL,
            to_emails=RECIPIENTS_EMAIL,
            subject=f'Сообщение через форму обратной связи от {feedback.email}',
            html_content=f'Дата и время отправки: {feedback.created_at}<br><br>'
                         f'Е-майл отправителя: {feedback.email}<br><br>'
                         f'Имя отправителя: {feedback.name}<br><br>'
                         f'Текст:<br>'
                         f'{feedback.message}<br>')
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        sg.send(message)

        return Response(status=200)
