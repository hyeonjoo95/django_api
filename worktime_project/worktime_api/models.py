from django.db import models

class WorkTimeLog(models.Model):
    user_id = models.IntegerField()
    date = models.DateField(null=False, blank=False)
    tag = models.CharField(max_length=15)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
       return self.tag

class WorkTime(models.Model):
    user_id = models.IntegerField()
    date = models.DateField(null=False, blank=False)
    in_time = models.DateTimeField(null=True, blank=True)
    out_time = models.DateTimeField(null=True, blank=True)
    total_work_time = models.IntegerField(default=0)
    total_rest_time = models.IntegerField(default=0)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
       return self.date
