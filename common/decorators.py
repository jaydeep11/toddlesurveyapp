"""Custom decorators"""
from functools import wraps
from django.conf import settings

from rest_framework.response import Response
from rest_framework import status, serializers

from common.authorization import Authorization

"""Decorator to check whether session is authorized"""
def session_authorize(*args, **kwargs):
    def deco(f):
        def abstract_session_token(request, **kwargs):
            session_token_header_key = 'HTTP_AUTHORIZATION'
            session_token = request.META.get(session_token_header_key)
            if not session_token:
                return Response({},status=status.HTTP_401_UNAUTHORIZED)
            session_token = session_token.split(" ")[1]
            return session_token

        @wraps(f)
        def decorated_function(*args, **kwargs):
            request = args[1]
            session_token = abstract_session_token(request)
            is_authorized = Authorization.authorize_token(session_token)
            if not is_authorized:
                return Response({},status=status.HTTP_401_UNAUTHORIZED)

            return f(*args, **kwargs)

        return decorated_function
    return deco

