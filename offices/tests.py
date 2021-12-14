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


class BuildingListViewTest(TestCase):
    def setUp(self):
        self.client = Client()

        building_1 = Building.objects.create(
            id=1,
            city        = 'a',
            district    = 'a',
            address     = 'a',
            latitude    = 0,
            longitude   = 0,
            name        = 'a',
            title       = 'a',
            sub_title   = 'a',
            description = 'a',
        )

        BuildingImage.objects.create(
            name     = 'a',
            url      = 'a',
            building = building_1
        )

        building_2 = Building.objects.create(
            id=2,
            city        = 'b',
            district    = 'b',
            address     = 'b',
            latitude    = 0,
            longitude   = 0,
            name        = 'b',
            title       = 'b',
            sub_title   = 'b',
            description = 'b',
        )

        BuildingImage.objects.create(
            name     = 'b',
            url      = 'b',
            building = building_2
        )

        office_1 = Office.objects.create(
            name         = 'a',
            building     = building_1,
            price        = 1,
            capacity     = 1,
            capacity_max = 100,
            image        = 'a'
        )

        office_2 = Office.objects.create(
            name         = 'b',
            building     = building_2,
            price        = 2,
            capacity     = 2,
            capacity_max = 200,
            image        = 'b'
        )

    def tearDown(self):
        Building.objects.all().delete()
        Office.objects.all().delete()
        BuildingImage.objects.all().delete()

    def test_building_list_view_get_method_without_query_without_order_success(self):
        response  = self.client.get('/buildings')

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.json(), {
            'MESSAGE': 'SUCCESS',
            'RESULT': {
                'count': 2,
                'buildings': [
                    {
                        'id'           : 1,
                        'name'         : 'a',
                        'city'         : 'a',
                        'district'     : 'a',
                        'image'        : 'a',
                        'min_capacity' : 1,
                        'max_capacity' : 100,
                        'min_price'    : '1.00',
                        'max_price'    : '1.00',
                        'latitude'     : '0.000000',
                        'longitude'    : '0.000000',
                    },
                    {
                        'id'           : 2,
                        'name'         : 'b',
                        'city'         : 'b',
                        'district'     : 'b',
                        'image'        : 'b',
                        'min_capacity' : 2,
                        'max_capacity' : 200,
                        'min_price'    : '2.00',
                        'max_price'    : '2.00',
                        'latitude'     : '0.000000',
                        'longitude'    : '0.000000',
                    },
                ]
            }
        })

    def test_building_list_view_get_method_with_query_without_order_success(self):
        response = self.client.get('/buildings?search=a')

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.json(), {
            'MESSAGE': 'SUCCESS',
            'RESULT': {
                'count': 1,
                'buildings': [
                    {
                        'id'           : 1,
                        'name'         : 'a',
                        'city'         : 'a',
                        'district'     : 'a',
                        'image'        : 'a',
                        'min_capacity' : 1,
                        'max_capacity' : 100,
                        'min_price'    : '1.00',
                        'max_price'    : '1.00',
                        'latitude'     : '0.000000',
                        'longitude'    : '0.000000',
                    },
                ]
            }
        })


    def test_building_list_view_get_method_without_query_with_order_success(self):
        response = self.client.get('/buildings?order-by=price-high')

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.json(), {
            'MESSAGE': 'SUCCESS',
            'RESULT': {
                'count': 2,
                'buildings': [
                    {
                        'id'           : 2,
                        'name'         : 'b',
                        'city'         : 'b',
                        'district'     : 'b',
                        'image'        : 'b',
                        'min_capacity' : 2,
                        'max_capacity' : 200,
                        'min_price'    : '2.00',
                        'max_price'    : '2.00',
                        'latitude'     : '0.000000',
                        'longitude'    : '0.000000',
                    },
                    {
                        'id'           : 1,
                        'name'         : 'a',
                        'city'         : 'a',
                        'district'     : 'a',
                        'image'        : 'a',
                        'min_capacity' : 1,
                        'max_capacity' : 100,
                        'min_price'    : '1.00',
                        'max_price'    : '1.00',
                        'latitude'     : '0.000000',
                        'longitude'    : '0.000000',
                    },
                ]
            }
        })

    def test_building_list_view_get_method_with_query_without_order_invalid_filter_error(self):
        response = self.client.get('/buildings?check-in=2021-12-12&check-out=2022-01-0')

        self.assertEqual(response.status_code, 400)

        self.assertEqual(response.json(), {'MESSAGE': 'INVALID_FILTER'})
