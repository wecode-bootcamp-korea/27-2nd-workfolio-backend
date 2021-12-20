import json, datetime, uuid

from django.views        import View
from django.http         import JsonResponse
from django.db           import transaction

from reservations.models import Reservation
from offices.models      import Office
from core.utils          import authorization


class ReservationView(View):
    @authorization
    def post(self, request):
        try:
            data = json.loads(request.body)
            user = request.user
            
            headcount          = data["head_count"]
            check_in           = data["check_in_date"]
            check_out          = data["check_out_date"]
            office             = data["office"]

            check_in  = datetime.date.fromisoformat(check_in)
            check_out = datetime.date.fromisoformat(check_out)

            if headcount > Office.objects.get(id=office).capacity_max:
                return JsonResponse({"Message": "EXCEEDING MAXIMUM OCCUPANCY"}, status=400)

            if check_in >= check_out:
                return JsonResponse({"Message": "Invalid Date"}, status=400)
            
            day_price   = Office.objects.get(id=office).price
            total_price = ((check_out - check_in).days + 1)*day_price

            with transaction.atomic():
                if user.point<=total_price:
                    return JsonResponse({"Message":"Insufficient points"}, status=400)

                user.point -= total_price
                user.save()
                
                reservations = Reservation.objects.filter(office_id=office)

                for reservation in reservations:
                    if not ((reservation.check_in_date < check_in and reservation.check_in_date <= check_out)\
                        or (reservation.check_out_date >= check_in and reservation.check_out_date > check_out)):
                        return JsonResponse({'Message' : 'RESERVATION_FAIL'}, status=400)

                Reservation.objects.create(
                    reservation_number = str(uuid.uuid4()),
                    headcount          = headcount,
                    check_in_date      = check_in,
                    check_out_date     = check_out,
                    user               = user,
                    office_id          = office,
                )
                return JsonResponse({"Message" : "CREATED"}, status = 201)

        except KeyError:
            return JsonResponse({"Message":"KEY_ERROR"}, status = 400)
        except ValueError:
            return JsonResponse({'Message': 'VALUE_ERROR'}, status = 400)

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