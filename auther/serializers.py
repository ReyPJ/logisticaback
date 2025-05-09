from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

        def validate(self, data):
            if User.objects.filter(email=data['email']).exists():
                raise serializers.ValidationError(
                    {"email": "This email is already in use"})
            return data

        def create(self, validated_data):
            user = User.objects.create_user(**validated_data)
            return user
