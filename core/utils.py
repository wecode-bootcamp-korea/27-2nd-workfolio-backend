import jwt
from django.http  import JsonResponse

from users.models import User
from my_settings  import ALGORITHM, SECRET_KEY

def authorization(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            bearer_token = request.headers['Authorization']

            if type(bearer_token) is not str:
                return JsonResponse({'MESSAGE': 'TOKEN_MUST_BE_STRING'}, status=401)

            bearer_token = bearer_token.split()

            if bearer_token[0] != 'Bearer':
                return JsonResponse({'MESSAGE': 'TOKEN_MUST_BE_BEARER'}, status=401)

            token = bearer_token[1]

            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

            request.user = User.objects.get(id=payload['id'])

            return func(self, request, *args, **kwargs)

        except KeyError:
            return JsonResponse({'MESSAGE': 'INVALID_TOKEN'}, status=401)

        except IndexError:
            return JsonResponse({'MESSAGE': 'INVALID_TOKEN'}, status=401)

        except jwt.exceptions.InvalidTokenError:
            return JsonResponse({'MESSAGE': 'INVALID_TOKEN'}, status=401)

        except User.DoesNotExist:
            return JsonResponse({'MESSAGE': 'INVALID_TOKEN'}, status=401)

    return wrapper
