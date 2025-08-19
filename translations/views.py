from asgiref.sync import async_to_sync
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from translations.services import get_supported_languages


# Create your views here.
class LanguagesViewSet(ViewSet):
    def list(self, request):
        languages = async_to_sync(get_supported_languages)()
        return Response(languages)
