from django.db import models
# from admin_doc.models import User
from django.contrib.auth import get_user_model
User = get_user_model()


GENDER_CHOICES = (
    ('R', 'Resolved'),
    ('NR', 'Not Resolved')
)
# Create your models here.
class diseaseJourney(models.Model):
    users= models.ForeignKey(User,on_delete=models.CASCADE,related_name='diseases')
    disease_name= models.CharField(max_length=100)
    month=models.IntegerField()
    years=models.IntegerField()
    duration = models.DurationField()
    status = models.CharField(max_length=2,choices=GENDER_CHOICES)
    journey_remark = models.TextField()