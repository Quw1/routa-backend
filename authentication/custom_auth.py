from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken


class CustomAuth(JWTAuthentication):
    def authenticate(self, request):
        res = super().authenticate(request)
        if res is not None:
            user, access = res

            if user.personal_token_secret != access['user_secret']:
                raise InvalidToken(
                    {
                        "detail": "Token is not valid",
                    }
                )
        return res
