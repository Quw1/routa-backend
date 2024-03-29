from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from rest_framework import serializers
from django.contrib import auth
from rest_framework_simplejwt.exceptions import TokenError

from .models import User
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')

        if not username.isalnum():
            raise serializers.ValidationError('The username must only contain alphabetic characters')

        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    username = serializers.EmailField(max_length=255, min_length=3, read_only=True)
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = User.objects.get(email=obj['email'])

        return {
            'access': user.tokens()['access'],
            'refresh': user.tokens()['refresh'],
        }

    class Meta:
        model = User
        fields = ['email', 'password', 'username', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        filtered_user_by_email = User.objects.filter(email=email)

        if filtered_user_by_email.exists() and filtered_user_by_email[0].auth_provider != 'email':
            raise AuthenticationFailed(
                detail=f'Please login via {filtered_user_by_email[0].auth_provider}'
            )

        user = auth.authenticate(email=email, password=password)

        if not user:
                raise AuthenticationFailed('INVALIDCRED')
        if not user.is_active:
            raise AuthenticationFailed('ACCDIS')
        if not user.is_verified:
            raise AuthenticationFailed('EMAILNOTVER')

        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens,
        }


class GetUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username']


class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=4)

    class Meta:
        fields = ['email']


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=uid)

            if not PasswordResetTokenGenerator().check_token(user=user, token=token):
                raise AuthenticationFailed('The reset link is invalid', 401)

            user.set_password(password)
            user.set_new_personal_secret()
            user.save()
            return user

        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid', 401)


# class LogoutSerializer(serializers.Serializer):
#     refresh = serializers.CharField(min_length=1, write_only=True)
#
#     default_error_messages = {
#         'bad_token': 'INVOREXP',
#     }
#
#     def validate(self, attrs):
#         self.refresh = attrs['refresh']
#         return attrs
#
#     def save(self, **kwargs):
#         try:
#             pass
#             # RefreshToken(self.refresh).blacklist()
#         except TokenError:
#             # raise ValidationError
#             self.fail('bad_token')

