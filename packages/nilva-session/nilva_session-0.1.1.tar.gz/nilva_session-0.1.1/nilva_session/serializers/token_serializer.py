from django.conf import settings
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import Token

from nilva_session.models import UserSession
from nilva_session.settings import DEFAULT


class TokenSessionObtainPairSerializer(TokenObtainPairSerializer):
    session_id_claim = getattr(settings, "USER_SESSION", {}).get("SESSION_ID_CLAIM", DEFAULT["SESSION_ID_CLAIM"])

    def get_token_by_session(cls, session: UserSession) -> Token:
        """
        Create and return a token for the given session.
        """
        token = super().get_token(session.user)
        token[cls.session_id_claim] = str(session.id)
        return token
