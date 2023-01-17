from rest_framework import serializers
from worktime_api.models import WorkTimeLog, WorkTime

class WorkTimeLogSerializer(serializers.ModelSerializer):
   class Meta:
       model = WorkTimeLog
       fields = ('user_id', 'date', 'tag', 'created')

class WorkTimeSerializer(serializers.ModelSerializer):
   class Meta:
       model = WorkTime
       fields = ('id', 'user_id', 'date', 'in_time', 'out_time', 'total_work_time', 'total_rest_time', 'updated')