from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Snippet


class SnippetSerializer(serializers.ModelSerializer):
   class Meta:
       model = Snippet
       fields = ['id', 'title', 'code', 'language', 'style']

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Это поле для пароля, оно будет доступно только для записи

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']  # Добавляем 'password' в список полей

    def create(self, validated_data):
        # Создаем пользователя с хешированием пароля
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user