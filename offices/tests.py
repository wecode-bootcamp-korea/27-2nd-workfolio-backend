from django.test         import TestCase, Client
from django.utils        import timezone

from .models             import Building, BuildingImage, Special, Office
from reservations.models import Reservation
from users.models        import User


class SpecialListTest(TestCase):
    def setUp(self):
        self.client = Client()
        Special.objects.create(name='asdf', description='asdf', icon='asdf')

    def test_success_speical_list_get_method(self):
        response = self.client.get('/buildings/specials')

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.json(), {
            'MESSAGE': 'SUCCESS',
            'RESULT': [
                'asdf'
            ]
        })

    def tearDown(self):
        Special.objects.all().delete()


class BuildingViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.date   = timezone.now().date()

        building  = Building.objects.create(
            id          = 1,
            name        = 'a',
            latitude    = 0.000000,
            longitude   = 0.000000,
            sub_title   = 'a',
            description = 'a',
            address     = 'a',
            title       = 'a',
            city        = 'a',
            district    = 'a',
            country     = 'a'
        )

        BuildingImage.objects.create(
            building = building,
            name     = 'a',
            url      = 'a'
        )

        building.specials.add(Special.objects.create(
            name        = 'a',
            description = 'a',
            icon        = 'a'
        ))

        office = Office.objects.create(
            id           = 1,
            building     = building,
            name         = 'a',
            price        = 0.00,
            capacity     = 0,
            capacity_max = 0,
            image        = 'a'
        )

        user = User.objects.create(
            name     = 'a',
            email    = 'a',
            point    = 100000,
            gender   = 'male',
            kakao_id = 'a'
        )

        Reservation.objects.create(
            user               = user,
            check_in_date      = self.date - timezone.timedelta(days=2),
            check_out_date     = self.date + timezone.timedelta(days=2),
            office             = office,
            headcount          = 3,
            reservation_number = 'asdf',
        )

        Reservation.objects.create(
            user               = user,
            check_in_date      = self.date - timezone.timedelta(days=4),
            check_out_date     = self.date - timezone.timedelta(days=2),
            office             = office,
            headcount          = 3,
            reservation_number = 'asdf',
        )

    def tearDown(self):
        Reservation.objects.all().delete()
        User.objects.all().delete()
        Office.objects.all().delete()
        Special.objects.all().delete()
        BuildingImage.objects.all().delete()
        Building.objects.all().delete()

    def test_building_view_get_method_success(self):
        response = self.client.get('/buildings/1')

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.json(), {
            'MESSAGE' : 'SUCCESS',
            'RESULT'  : {
                'id'        : 1,
                'name'      : 'a',
                'latitude'  : '0.000000',
                'longitude' : '0.000000',
                'city'      : 'a',
                'district'  : 'a',
                'address'   : 'a',
                'specials'  : [
                    {
                        'name'        : 'a',
                        'description' : 'a',
                        'icon'        : 'a',
                    }
                ],
                'images': [
                    {
                        'name' : 'a',
                        'url'  : 'a',
                    }
                ],
                'sub_title'   : 'a',
                'description' : 'a',
                'title'       : 'a',
                'offices'     : [
                    {
                        'id'           : 1,
                        'name'         : 'a',
                        'price'        : '0.00',
                        'capacity'     : 0,
                        'capacity_max' : 0,
                        'image'        : 'a',
                        'reservations' : [
                            [
                                str(self.date-timezone.timedelta(days=2)),
                                str(self.date+timezone.timedelta(days=2)),
                            ]
                        ]
                    }
                ]
            }
        })

    def test_building_view_get_method_404_error(self):
        response = self.client.get('/buildings/2')

        self.assertEqual(response.status_code, 404)

        self.assertEqual(response.json(), {
            'MESSAGE': 'INVALID_BUILDING_ID'
        })
