import jwt

from django.test    import TestCase, Client
from django.utils   import timezone

from .models        import Reservation
from offices.models import Office, Building
from users.models   import User
from my_settings    import ALGORITHM, SECRET_KEY


class ReservationViewTest(TestCase):
    def setUp(self):
        access_token = jwt.encode({'id': 1}, SECRET_KEY, ALGORITHM)
        header       = {'HTTP_Authorization': f'Bearer {access_token}'}
        self.client  = Client(**header)
        self.date    = timezone.now().date()

        building = Building.objects.create(
            id          = 1,
            name        = 'a',
            title       = 'a',
            sub_title   = 'a',
            description = 'a',
            address     = 'a',
            country     = 'a',
            city        = 'a',
            district    = 'a',
            latitude    = 0.000000,
            longitude   = 0.000000
        )

        office = Office.objects.create(
            id           = 1,
            building     = building,
            name         = 'a',
            price        = 1000,
            capacity     = 0,
            capacity_max = 0,
            image        = 'a'
        )

        user = User.objects.create(
            id       = 1,
            name     = 'a',
            email    = 'a',
            point    = 1000000,
            gender   = 'a',
            kakao_id = 'a'
        )

        Reservation.objects.create(
            id                 = 1,
            office             = office,
            user               = user,
            check_in_date      = self.date,
            check_out_date     = self.date + timezone.timedelta(days=1),
            headcount          = 10,
            reservation_number = 'a'
        )

        Reservation.objects.create(
            id                 = 2,
            office             = office,
            user               = user,
            check_in_date      = self.date - timezone.timedelta(days=9),
            check_out_date     = self.date - timezone.timedelta(days=3),
            headcount          = 10,
            reservation_number = 'b'
        )

    def tearDown(self):
        Reservation.objects.all().delete()
        User.objects.all().delete()
        Office.objects.all().delete()
        Building.objects.all().delete()

    def test_reservation_view_get_method_success(self):
        response = self.client.get('/reservations')

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.json(), {
            'MESSAGE' : 'SUCCESS',
            'RESULT'  : [
                {
                    'id'                 : 2,
                    'reservation_number' : 'b',
                    'building_id'        : 1,
                    'building_name'      : 'a',
                    'office_name'        : 'a',
                    'office_image'       : 'a',
                    'check_in_date'      : str(self.date-timezone.timedelta(days=9)),
                    'check_out_date'     : str(self.date-timezone.timedelta(days=3)),
                    'headcount'          : 10,
                    'total_price'        : '7000.00',
                    'is_deleted'         : False
                },
                {
                    'id'                 : 1,
                    'reservation_number' : 'a',
                    'building_id'        : 1,
                    'building_name'      : 'a',
                    'office_name'        : 'a',
                    'office_image'       : 'a',
                    'check_in_date'      : str(self.date),
                    'check_out_date'     : str(self.date+timezone.timedelta(days=1)),
                    'headcount'          : 10,
                    'total_price'        : '2000.00',
                    'is_deleted'         : False
                }

            ]
        })
