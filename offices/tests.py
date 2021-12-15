from django.test import TestCase, Client

from offices.models import Special

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
