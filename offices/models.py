from django.db import models


class Building(models.Model):
    name        = models.CharField(max_length=50)
    address     = models.CharField(max_length=100)
    country     = models.CharField(max_length=50)
    city        = models.CharField(max_length=50)
    district    = models.CharField(max_length=50)
    title       = models.CharField(max_length=100)
    sub_title   = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    latitude    = models.DecimalField(max_digits=9, decimal_places=6)
    longitude   = models.DecimalField(max_digits=9, decimal_places=6)
    specials    = models.ManyToManyField('Special', related_name='buildings')

    class Meta:
        db_table = 'buildings'

    def __str__(self):
        return self.name


class Office(models.Model):
    name         = models.CharField(max_length=50)
    price        = models.DecimalField(max_digits=10, decimal_places=2)
    building     = models.ForeignKey('Building', on_delete=models.CASCADE)
    capacity     = models.PositiveSmallIntegerField()
    capacity_max = models.PositiveSmallIntegerField()
    image        = models.CharField(max_length=500)

    class Meta:
        db_table = 'offices'
    
    def __str__(self):
        return self.name


class Special(models.Model):
    name        = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    icon        = models.CharField(max_length=50)

    class Meta:
        db_table = 'specials'
    
    def __str__(self):
        return self.name


class BuildingImage(models.Model):
    name     = models.CharField(max_length=50)
    url      = models.CharField(max_length=500)
    building = models.ForeignKey('Building', on_delete=models.CASCADE)

    class Meta:
        db_table = 'building_images'
    
    def __str__(self):
        return self.name