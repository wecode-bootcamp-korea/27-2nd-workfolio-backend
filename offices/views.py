import datetime

from django.views           import View
from django.http            import JsonResponse
from django.db.models       import F, Max, Min, Q, Count, Prefetch
from django.core.exceptions import ValidationError
from django.utils           import timezone

from offices.models         import Building, Office, Special
from reservations.models    import Reservation

def special_list(request):
    specials = Special.objects.all()

    result = [
        special.name
        for special in specials
    ]

    return JsonResponse({'MESSAGE': 'SUCCESS', 'RESULT': result}, status=200)


class BuildingView(View):
    def get(self, request, building_id):
        try:
            building = Building.objects.prefetch_related(
                'buildingimage_set',
                'specials',
                'office_set',
                Prefetch(
                    'office_set__reservation_set',
                    queryset = Reservation.objects.filter(
                        check_out_date__gte = timezone.now().date()
                    ),
                )
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
                        'image'        : office.image,
                        'reservations' : [
                            [
                                reservation.check_in_date,
                                reservation.check_out_date
                            ]
                            for reservation in office.reservation_set.all()
                        ]
                    }
                    for office in building.office_set.all()
                ],
            }

            return JsonResponse({'MESSAGE': 'SUCCESS', 'RESULT': result}, status=200)

        except Building.DoesNotExist:
            return JsonResponse({'MESSAGE': 'INVALID_BUILDING_ID'}, status=404)


class BuildingListView(View):
    def get(self, request):
        try:
            data  = request.GET

            orders = {
                'price-low'      : 'min_price',
                'price-high'     : '-min_price',
                'popularity'     : '-popularity',
                'headcount-low'  : 'min_capacity',
                'headcount-high' : '-max_capacity'
            }

            filters = {
                'special' : 'specials__name__in',
                'country' : 'country__in',
                'city'    : 'city__in',
                'district': 'district__in'
            }

            limit        = int(data.get('limit', 10) or 10)
            offset       = int(data.get('offset', 0) or 0)
            check_in     = data.get('check-in', None)
            check_out    = data.get('check-out', None)
            max_price    = int(data.get('max-price', 50000) or 50000)
            min_price    = int(data.get('min-price', 0) or 0)
            capacity     = int(data.get('headcount', 10) or 10)
            order_by     = data.get('order-by', None)
            order_by     = orders[order_by] if order_by in orders else 'id'

            filter_set   = {
                filters.get(key): value
                for (key, value) in dict(request.GET).items()\
                if filters.get(key) and value != ['']
            }

            search = data.get('search', None)

            if search:
                filter_set['name__contains'] = search

            offices = Office.objects.exclude(
                Q(
                    Q(reservation__check_out_date__gt=check_in) &
                    Q(reservation__check_in_date__lte=check_in)
                ) |
                Q(reservation__check_in_date__range=[
                    check_in,
                    datetime.date.fromisoformat(check_out) - datetime.timedelta(days=1)
                ])
            ).values_list('id')\
            if check_in and check_out else Office.objects.all().values_list('id')

            office_ids = [office[0] for office in offices]

            buildings = Building.objects.filter(
                office__id__in = office_ids
            ).distinct().annotate(
                max_price      = Max(F('office__price')),
                min_price      = Min(F('office__price')),
                max_capacity   = Max(F('office__capacity_max')),
                min_capacity   = Min(F('office__capacity')),
                popularity     = Count(F('office__reservation')),
            ).prefetch_related('buildingimage_set').filter(
                max_price__gte    = min_price,
                min_price__lte    = max_price,
                max_capacity__gte = capacity,
                min_capacity__lte = capacity,
                **filter_set,
            ).order_by(order_by)

            result = {
                'count': buildings.count(),
                'buildings': [
                    {
                        'id'           : building.id,
                        'name'         : building.name,
                        'city'         : building.city,
                        'district'     : building.district,
                        'image'        : building.buildingimage_set.all()[0].url,
                        'min_capacity' : building.min_capacity,
                        'max_capacity' : building.max_capacity,
                        'min_price'    : building.min_price,
                        'max_price'    : building.max_price,
                        'latitude'     : building.latitude,
                        'longitude'    : building.longitude,
                    }
                    for building in buildings[offset:offset+limit]
                ]
            }

            return JsonResponse({'MESSAGE': 'SUCCESS', 'RESULT': result}, status=200)

        except ValueError:
            return JsonResponse({'MESSAGE': 'INVALID_FILTER'}, status=400)
