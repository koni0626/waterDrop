from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class AttendTable(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    startDate = models.DateTimeField()
    endDate = models.DateTimeField()

    def get_startDate(self):
        return self.startDate

    def get_endDate(self):
        return self.endDate