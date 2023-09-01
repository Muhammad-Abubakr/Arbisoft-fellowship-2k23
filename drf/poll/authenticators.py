from base64 import urlsafe_b64decode
import jwt, datetime

from django.contrib.auth.models import User

from rest_framework.authentication import TokenAuthentication, BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed


class BearerAuthentication(TokenAuthentication):
    keyword = 'Bearer'
    
