from rest_framework import serializers

from .models import Dictionary, Word


class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = ["id", "word", "translation"]


class DictionarySerializer(serializers.ModelSerializer):
    words = WordSerializer(many=True, read_only=True)

    class Meta:
        model = Dictionary
        fields = ["id", "name", "source_lang", "target_lang", "words"]
