from aiogram.utils.web_app import check_webapp_signature, safe_parse_webapp_init_data
from django.conf import settings
from django.contrib.auth import login
from django.http import JsonResponse
from pydantic import BaseModel
from rest_framework.views import APIView

from .models import User


class InitRequest(BaseModel):
    tgWebAppData: str


# Create your views here.
class UserView(APIView):
    def post(self, request):
        body = request.data
        data = body.get('tgWebAppData', None)
        if not data:
            return JsonResponse({"message": "Unauthorized"}, status=401)

        if check_webapp_signature(settings.TELEGRAM_BOT_TOKEN, data):
            user_telegram_id = safe_parse_webapp_init_data(settings.TELEGRAM_BOT_TOKEN, data).user.id
            user = User.objects.get(telegram_id=user_telegram_id)
            login(request, user)
            return JsonResponse({"message": "Success"})

        return JsonResponse({"message": "Unauthorized"}, status=401)
