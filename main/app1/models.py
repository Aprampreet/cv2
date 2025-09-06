from django.db import models
from django.contrib.auth.models import User

class DailyPostureScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()   
    score = models.IntegerField(default=0)

    class Meta:
        unique_together = ('user', 'date')

    def __str__(self):
        return f"{self.user} - {self.date} - {self.score}"
