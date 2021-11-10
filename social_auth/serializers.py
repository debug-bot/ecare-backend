from pyasn1.type.univ import Null
from rest_framework import serializers
from . import google, facebook, twitterhelper
from .register import register_social_user
import os
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.conf import settings


class FacebookSocialAuthSerializer(serializers.Serializer):
    """Handles serialization of facebook related data"""
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = facebook.Facebook.validate(auth_token)
        try:
            user_id = user_data['id']
            email = user_data['email']
            name = user_data.get('name', '')
            picture = user_data.get('picture', None)
            birthday = user_data.get('birthday', None)
            provider = 'facebook'
            return register_social_user(
                provider=provider,
                user_id=user_id,
                email=email,
                name=name,
                picture=picture,
                birthday=birthday
            )
        except Exception as identifier:

            raise serializers.ValidationError(
                str(identifier) +
                'The token  is invalid or expired. Please login again.'
            )


class GoogleSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = google.Google.validate(auth_token)
        try:
            user_data['sub']
        except:
            raise serializers.ValidationError(
                'The token is invalid or expired. Please login again.'
            )

        if user_data['aud'] != settings.GOOGLE_CLIENT_ID:

            raise AuthenticationFailed('oops, who are you?')

        user_id = user_data['sub']
        email = user_data['email']
        name = user_data.get('name', '')
        picture = user_data.get('picture', None)
        birthday = user_data.get('birthday', None)
        provider = 'google'

        return register_social_user(
            provider=provider, user_id=user_id, email=email, name=name, picture=picture, birthday=birthday)


class TwitterAuthSerializer(serializers.Serializer):
    """Handles serialization of twitter related data"""
    access_token_key = serializers.CharField()
    access_token_secret = serializers.CharField()

    def validate(self, attrs):

        access_token_key = attrs.get('access_token_key')
        access_token_secret = attrs.get('access_token_secret')

        user_info = twitterhelper.TwitterAuthTokenVerification.validate_twitter_auth_tokens(
            access_token_key, access_token_secret)

        try:
            user_id = user_info['id_str']
            email = user_info['email']
            name = user_info['name']
            provider = 'twitter'
        except:
            raise serializers.ValidationError(
                'The tokens are invalid or expired. Please login again.'
            )

        return register_social_user(
            provider=provider, user_id=user_id, email=email, name=name)
