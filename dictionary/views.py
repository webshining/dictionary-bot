from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .serializers import DictionarySerializer


# Create your views here.
class DictionaryViewSet(ModelViewSet):
    serializer_class = DictionarySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.dictionaries.all()

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)
