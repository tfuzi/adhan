from django.db import models

class Data(models.Model):
    ip = models.CharField(max_length=100, blank=True, null=True)
    hadith = models.TextField(blank=True, null=True)
    notice = models.TextField(blank=True, null=True)
    fajarAdhan = models.CharField(max_length=100, blank=True, null=True)
    fajarIqama = models.CharField(max_length=100, blank=True, null=True)
    fajarEnds = models.CharField(max_length=100, blank=True, null=True)
    duhurAdhan = models.CharField(max_length=100, blank=True, null=True)
    duhurIqama = models.CharField(max_length=100, blank=True, null=True)
    duhurEnds = models.CharField(max_length=100, blank=True, null=True)
    asarAdhan = models.CharField(max_length=100, blank=True, null=True)
    asarIqama = models.CharField(max_length=100, blank=True, null=True)
    asarEnds = models.CharField(max_length=100, blank=True, null=True)
    maghribAdhan = models.CharField(max_length=100, blank=True, null=True)
    maghribIqama = models.CharField(max_length=100, blank=True, null=True)
    maghribEnds = models.CharField(max_length=100, blank=True, null=True)
    ishaAdhan = models.CharField(max_length=100, blank=True, null=True)
    ishaIqama = models.CharField(max_length=100, blank=True, null=True)
    ishaEnds = models.CharField(max_length=100, blank=True, null=True)
    sunrise = models.CharField(max_length=100, blank=True, null=True)
    sunset = models.CharField(max_length=100, blank=True, null=True)
    audio = models.CharField(max_length=100, blank=True, null=True)
    school = models.CharField(max_length=100, blank=True, null=True)
    zipcode = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    time_difference = models.DurationField(blank=True, null=True)
    user_date_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.ip