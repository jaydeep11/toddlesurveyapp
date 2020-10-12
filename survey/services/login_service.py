"""User Session Service."""
from ..models import Token
from django.utils.crypto import get_random_string
import jwt

class UserSessionService(object):
    """User Session Service."""

    def __init__(self, session_input):
        #process session input for validating whether username and password are valid or not
        self._create_new_session_token()

    def __generate_session_token(self):
        """Generate a random token"""

        return get_random_string(length=32)

    def _create_new_session_token(self):
        """
        Create new session token.

        Create a new Login Object.
        """
        session_token = self.__generate_session_token()
        payload = {
            'token' : session_token
        }
        self.encoded_token = jwt.encode(payload, 'secret', algorithm='HS256')
        Token.objects.create(session_token=session_token)

    def session_success_data(self):
        """Generate a dictionary from a Login Object."""
        return {
            'id_token': self.encoded_token,
        }
