from django.views        import View
from django.http         import JsonResponse
from django.utils        import timezone

from offices.models      import Building
from reservations.models import Reservation


class BuildingView(View):
    def get(self, request, building_id):
        try:
            building = Building.objects.prefetch_related(
                'buildingimage_set',
                'specials',
                'office_set'
            ).get(id=building_id)

            result = {
                'id'        : building_id,
                'name'      : building.name,
                'latitude'  : building.latitude,
                'longitude' : building.longitude,
                'city'      : building.city,
                'district'  : building.district,
                'address'   : building.address,
                'specials'  : [
                    {
                        'name'        : special.name,
                        'description' : special.description,
                        'icon'        : special.icon
                    }
                    for special in building.specials.all()
                ],
                'images': [
                    {
                        'name' : image.name,
                        'url'  : image.url
                    }
                    for image in building.buildingimage_set.all()
                ],
                'sub_title'   : building.sub_title,
                'description' : building.description,
                'title'       : building.title,
                'offices'     : [
                    {
                        'id'           : office.id,
                        'name'         : office.name,
                        'price'        : office.price,
                        'capacity'     : office.capacity,
                        'capacity_max' : office.capacity_max,
                        'image'        : office.image
                    }
                    for office in building.office_set.all()
                ]
            }

            return JsonResponse({'MESSAGE': 'SUCCESS', 'RESULT': result}, status=200)

        except Building.DoesNotExist:
            return JsonResponse({'MESSAGE': 'INVALID_BUILDING_ID'}, status=404)


class PlaceListView(View):
    def get(self, request):
        cities    = Building.objects.filter(country='한국')
        countries = Building.objects.exclude(country='한국')

        cities    = [*set(building.city for building in cities)]
        countries = [*set(building.country for building in countries)]

        result = {
            'cities'    : cities,
            'countries' : countries
        }

        return JsonResponse({'MESSAGE': 'SUCCESS', 'RESULT': result}, status=200)
