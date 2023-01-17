
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import WorkTimeLogSerializer, WorkTimeSerializer
from .models import WorkTimeLog, WorkTime
from rest_framework import status
import datetime

class WorkDate():
    def getWorkDate(now):
        today = now.strftime('%Y-%m-%d')
        yesterday = (now - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        arrToday = today.split('-')

        todayStart = datetime.datetime(int(arrToday[0]),int(arrToday[1]),int(arrToday[2]),6,0,0)
        if now < todayStart:
            date = yesterday
        else:
            date = today
        
        return date
    
    def changeTypeToDatetime(date):
        date = date.strftime('%Y/%m/%d/%H/%M/%S').split('/')
        date = datetime.datetime(int(date[0]),int(date[1]),int(date[2]),int(date[3]),int(date[4]),int(date[5]))

        return date

class WorkTimeRecordAPIView(APIView):
    def post(self, request):     
        reqData = request.data

        now = datetime.datetime.now()
        date = WorkDate.getWorkDate(now)

        lastLogData = WorkTimeLog.objects.filter(user_id=reqData['user_id'], date=date).order_by('created').last()
        if reqData['tag'] == 'IN':    
            if lastLogData == None:
                WorkTime.objects.create(user_id=reqData['user_id'], date=date, in_time=now)
            elif lastLogData.tag != 'IN':
                logCreated = WorkDate.changeTypeToDatetime(lastLogData.created)
                timeDiff = now - logCreated

                worktimeData = WorkTime.objects.get(user_id=reqData['user_id'], date=date)
                total_rest_time = (timeDiff.seconds / 60) + worktimeData.total_rest_time
                WorkTime.objects.filter(user_id=reqData['user_id'], date=date).update(out_time=None, total_work_time=0, total_rest_time=total_rest_time)     
        elif reqData['tag'] == 'OUT':
            if lastLogData != None and lastLogData.tag != 'OUT':
                worktimeData = WorkTime.objects.get(user_id=reqData['user_id'], date=date)

                inTime = WorkDate.changeTypeToDatetime(worktimeData.in_time)
                timeDiff = now - inTime

                totalWorkTime = (timeDiff.seconds / 60) - worktimeData.total_rest_time
                if totalWorkTime < 0: totalWorkTime = 0

                WorkTime.objects.filter(user_id=reqData['user_id'], date=date).update(out_time=now, total_work_time=totalWorkTime)
        
        reqData['date'] = date
        worktimeLogSerializer = WorkTimeLogSerializer(data=reqData)
        if worktimeLogSerializer.is_valid():
            worktimeLogSerializer.save()
        
        return Response(worktimeLogSerializer.data, status=status.HTTP_201_CREATED)

class WorkTimeListAPIView(APIView):
    def get(self, request, user_id):
        now = datetime.datetime.now()
        date = WorkDate.getWorkDate(now)

        worktimeData = list(WorkTime.objects.filter(user_id=user_id).order_by('-date'))
        recentData = worktimeData[0]
        if recentData != None and recentData.date.strftime('%Y-%m-%d') == date and recentData.out_time is None:
            inTime = WorkDate.changeTypeToDatetime(recentData.in_time)
            timeDiff = now - inTime
            totalWorkTime = (timeDiff.seconds / 60) - recentData.total_rest_time
            recentData.total_work_time = totalWorkTime
            
        return Response(WorkTimeSerializer(worktimeData, many=True).data, status=status.HTTP_200_OK)

class WorkTimeDetailAPIView(APIView):
    def get(self, request, pk):
        worktime = WorkTime.objects.get(id=pk)
        return Response(WorkTimeSerializer(worktime).data, status=status.HTTP_201_CREATED)

    def put(self, request, pk):
        reqData = request.data
        data = WorkTime.objects.get(id=pk)
        serializer = WorkTimeSerializer(instance=data, data=reqData)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        data = WorkTime.objects.get(id=pk)
        data.delete()
        return Response("delete ok", status=status.HTTP_200_OK) 
        