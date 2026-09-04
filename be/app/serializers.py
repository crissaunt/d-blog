from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import BlogPost

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'role', 'is_staff', 'date_joined')
        read_only_fields = ('id', 'is_staff', 'date_joined')


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6, style={'input_type': 'password'})
    password_confirm = serializers.CharField(write_only=True, min_length=6, style={'input_type': 'password'}, required=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'password_confirm', 'role')
        extra_kwargs = {
            'email': {'required': True},
            'role': {'required': False},
        }

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.pop('password_confirm', None)

        if password_confirm is not None and password != password_confirm:
            raise serializers.ValidationError({"password_confirm": "Passwords do not match."})

        if User.objects.filter(email__iexact=attrs.get('email')).exists():
            raise serializers.ValidationError({"email": "A user with that email already exists."})

        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class BlogPostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = BlogPost
        fields = (
            'id',
            'title',
            'content',
            'author',
        )
        read_only_fields = ('id', 'author')


