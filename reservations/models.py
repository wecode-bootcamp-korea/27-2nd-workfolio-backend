from django.db import models

from core.models import TimeStampModel

class Reservation(TimeStampModel):
    reservation_number = models.CharField(max_length=50)
    headcount          = models.PositiveSmallIntegerField()
    check_in_date      = models.DateField()
    check_out_date     = models.DateField()
    is_deleted         = models.BooleanField(default=False)
    user               = models.ForeignKey('users.User', on_delete=models.CASCADE)
    office             = models.ForeignKey('offices.Office', on_delete=models.CASCADE)

    class Meta:
        db_table = 'reservations'

    def __str__(self):
        return self.reservation_number