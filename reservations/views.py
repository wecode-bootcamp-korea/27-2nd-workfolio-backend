from django.views        import View
from django.http         import JsonResponse

from reservations.models import Reservation

from core.utils          import authorization


class ReservationView(View):
    @authorization
    def get(self, request):
        user = request.user

        reservations = Reservation.objects.select_related(
            'office', 'office__building'
        ).filter(user=user).order_by('check_in_date')

        result = [
            {
                'id'                 : reservation.id,
                'reservation_number' : reservation.reservation_number,
                'building_id'        : reservation.office.building.id,
                'building_name'      : reservation.office.building.name,
                'office_name'        : reservation.office.name,
                'office_image'       : reservation.office.image,
                'check_in_date'      : reservation.check_in_date,
                'check_out_date'     : reservation.check_out_date,
                'headcount'          : reservation.headcount,
                'total_price'        : (
                    (reservation.check_out_date-reservation.check_in_date).days+1
                )*reservation.office.price,
                'is_deleted'         : reservation.is_deleted,
            }
            for reservation in reservations
        ]

        return JsonResponse({'MESSAGE': 'SUCCESS', 'RESULT': result}, status=200)
