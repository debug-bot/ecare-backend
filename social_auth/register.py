
from django.contrib.auth import authenticate
from app.models import User
import os
import random
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings

def register_social_user(provider, user_id, email, name, picture, birthday):
    if provider == 'facebook':
        picture = picture['data']['url']
    filtered_user_by_email = User.objects.filter(email=email)
    full_name = name.split()
    first_name = full_name[0]
    try:
        middle_name = full_name[1]
    except:
        middle_name = ''
    try:
        last_name = ' '.join(full_name[2:])
    except:
        last_name = ''
    if filtered_user_by_email.exists():

        if provider == filtered_user_by_email[0].auth_provider:

            registered_user = authenticate(request=None,
                                           email=email, password=settings.SOCIAL_SECRET)
            user = filtered_user_by_email[0]

            user.first_name = first_name
            user.middle_name = middle_name
            user.last_name = last_name
            #user.profile_pic = picture
            user.date_of_birth = birthday
            user.save()

            return {
                'email': registered_user.email,
                'first_name': first_name, 'middle_name': middle_name,
                'last_name': last_name, 'profile_pic': picture, 'date_of_birth': birthday,
                'tokens': registered_user.tokens()}

        else:
            raise AuthenticationFailed(
                detail='Please continue your login using ' + filtered_user_by_email[0].auth_provider)

    else:
        user = {'email': email,
                'password': settings.SOCIAL_SECRET}
        user = User.objects.create_user(**user)
        user.is_verified = True
        user.auth_provider = provider
        user.first_name = first_name
        user.middle_name = middle_name
        user.last_name = last_name
        #user.profile_pic = picture
        user.date_of_birth = birthday
        user.save()

        new_user = authenticate(request=None,
                                email=email, password=settings.SOCIAL_SECRET)
        return {
            'email': new_user.email,
            'first_name': first_name, 'middle_name': middle_name,
            'last_name': last_name, 'profile_pic': picture, 'date_of_birth': birthday,
            'tokens': new_user.tokens()
        }
