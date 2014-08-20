from django.db import models


class Sample(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='img')


class SurveryResult(models.Model):
    sample = models.ForeignKey(Sample)
