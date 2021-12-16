from unittest.mock import MagicMock, patch

from django.test   import Client, TestCase

from users.models import User

class KakaoLogInTest(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        User.objects.all().delete()

    @patch("core.kakao.requests")
    def test_kakao_login_success(self, mocked_requests):
        client = Client()

        class MockedResponse:
            def __init__(self):
                self.status_code=200

            def json(self):
                return {
                    "id":2032245202,
                    "connected_at":"2021-12-13T13:14:17Z",
                    "properties":{
                        "nickname":"양주영"
                    },

                    "kakao_account":{
                        "profile_nickname_needs_agreement":False,
                        "profile":{
                            "nickname":"양주영"
                        },
                        "has_email":True,
                        "email_needs_agreement":False,
                        "is_email_valid":True,
                        "is_email_verified":True,
                        "email":"wndun21@daum.net",
                        "has_birthday":True,
                        "birthday_needs_agreement":True,
                        "has_gender":True,
                        "gender_needs_agreement":False,
                        "gender":"female",
                    }
                }
        mocked_requests.get = MagicMock(return_value = MockedResponse())
        headers             = {"HTTP_Authorization": "가짜 access_token"}
        response            = client.post("/users/login", **headers)
        print(response)

        self.assertEqual(response.status_code, 200)