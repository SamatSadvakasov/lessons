from rest_framework import serializers
from .models import Book

class BookModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            'title',
            'author',
            'summary',
            'isbn',
            'display_genre',
            'language'
        ]