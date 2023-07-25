from rest_framework import serializers
from .models import Todo


class TodoSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Todo
        fields = '__all__'