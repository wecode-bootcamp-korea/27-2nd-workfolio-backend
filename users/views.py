import json
import jwt

from django.views           import View
from django.http            import JsonResponse
from django.core.exceptions import ValidationError

from users.models           import User

from my_settings            import SECRET_KEY, ALGORITHM

from core.kakao             import KakaoAPI


class KakaoLogInView(View):
    def post(self, request):
        try:
            kakao_token   = request.headers['Authorization']
            kakao_user    = KakaoAPI(kakao_token).get_kakao_user()
            kakao_account = kakao_user['kakao_account']

            kakao_id = kakao_user['id']
            name     = kakao_account['profile']["nickname"]
            email    = kakao_account['email']
            gender   = kakao_account['gender']

            user, created = User.objects.get_or_create(
                kakao_id  = kakao_id,
                name      = name,
                email     = email,
                gender    = gender,
                defaults  =  {
                    'point'  : 150000
                }
            )
            
            access_token = jwt.encode({'id' : user.id}, SECRET_KEY, ALGORITHM)

            return JsonResponse({"message": "SUCCESS","access_token" : access_token}, status=200)
        
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
        
        except ValidationError as e:
            return JsonResponse({'MESSAGE': e.message}, status=400)