from collections import Counter

from django.http import JsonResponse
from django import forms
from rest_framework import serializers

from datetime import datetime, timedelta

from login.models import *      #login.models
import json


# This is the timerange form, including start time and end time
class TimeForm(forms.Form):
    start_time = datetime.now().replace(minute=0, second=0, microsecond=0)
    end_time = start_time + timedelta(hours=24)

    # Add a time form which can choose the time
    start_time_form = forms.DateTimeField(
        label='预约开始时间',
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local', 'min': start_time, 'max': end_time}
        )
    )
    end_time_form = forms.DateTimeField(
        label='预约结束时间',
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local', 'min': start_time + timedelta(hours=1), 'max': end_time}
        )
    )


# 使用Serializer序列化数据，直接返回json数据即可
class RoomSerializerForStudent(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'name', 'capacity', 'open_time', 'close_time']


# Rooms students can see
def stu_room_available(request):
    print("in room_available")
    data = json.loads(request.body.decode('utf-8'))       #如果获取的数据是none就加一下
    qtype = data.get('type')
    if qtype == 'admin':
        room_query_set = Room.objects.all()      #显示所有
    else:
        room_query_set = Room.objects.filter(is_active=1)
    room_serializer = RoomSerializerForStudent(room_query_set, many=True)
    room_data = room_serializer.data
    return JsonResponse({"room_list": room_data}, safe=False)


class SeatSerializerForStudent(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ['seat_id', 'pos', 'type', 'state']        #这里改了(这里需要加一个room_id,目前是写死了)


def seat(request):
    print("in seat")

    if request.method == "GET":
        room_id = request.GET.get('room_id')
        room_obj = Room.objects.get(id=room_id)
        print(room_obj)
        room_list = Room.objects.all()
        room_id = request.GET.get('room_id')
        if room_id:
            room = Room.objects.get(id=room_id)
            if room.is_active:
                seat_query_set = Seat.objects.filter(room=room)
                seat_serializer = SeatSerializerForStudent(seat_query_set, many=True)
                seat_data = seat_serializer.data
                return JsonResponse({"seat_list": seat_data}, safe=False)
            else:
                return JsonResponse({"status": "error", "msg": "该自习室已被关闭！"})
    elif request.method == "POST":
        # search for seat
        data = json.loads(request.body.decode('utf-8'))       #如果获取的数据是none就加一下
        room_id = data.get('room_id')
        seat_list = Seat.objects.filter(room_id=room_id)
        room_obj = Room.objects.get(id=room_id)
        print(room_obj.open_time.hour)
        '''
        seat_type = request.POST.get('type')
        seat_pos = request.POST.get('pos')
        seat_room = request.POST.get('room_id')
        seat_list = Seat.objects.all()
        if seat_type is not None:
            seat_list = seat_list.filter(type=seat_type)
        if seat_pos is not None:
            seat_list = seat_list.filter(pos=seat_pos)
        if seat_room is not None:
            seat_list = seat_list.filter(room=seat_room)
        '''
        seat_serializer = SeatSerializerForStudent(seat_list, many=True)
        seat_data = seat_serializer.data
        return JsonResponse({"seat_list": seat_data,"open":room_obj.open_time.hour,"close":room_obj.close_time.hour}, safe=False)

    else:
        return JsonResponse({"status": "error", "msg": "请求方法错误！"})
#获取特定的位置
def cseat(request):
    print("certain seat")

    if request.method == "POST":
        # search for seat
        data = json.loads(request.body.decode('utf-8'))       #如果获取的数据是none就加一下
        room_id = data.get('room_id')
        stype = data.get('type')
        seat_list = Seat.objects.filter(room_id=room_id,type = stype)

        seat_serializer = SeatSerializerForStudent(seat_list, many=True)
        seat_data = seat_serializer.data
        return JsonResponse({"seat_list": seat_data}, safe=False)

    else:
        return JsonResponse({"status": "error", "msg": "请求方法错误！"})

#预约座位
def exe_reservation(request):
    
    print("in reservation")
    '''
    username = request.META.get('HTTP_USERNAME')
    stu_id = Student.objects.get(name=username).id
    student_obj = Student.objects.get(id=stu_id)
    #print(username,stu_id,student_obj)
    '''    

    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))       #如果获取的数据是none就加一下
        '''
        room_id = request.POST.get('room_id')
        seat_id = request.POST.get('seat_id')
        the_seat = Seat.objects.get(room_id=room_id, pos=seat_id)
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        '''
        room_id = data.get('room_id')
        seat_id = data.get('seat_id')
        id = data.get('sid')
        student_obj = Student.objects.get(id=id)             
        #the_seat = Seat.objects.get(id=room_id, seat_id=seat_id)
        #print(the_seat)
        start_time = data.get('start_time')
        end_time = data.get('end_time')

        
        # transform the time format
        start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        end_time = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")

        print(start_time,end_time)
        # Check if the person has a reservation
        if Reservation.objects.filter(student=student_obj, seat_id=seat_id).exclude(status=3).exists():           #当前座位有预约了,seat_id为seat表的id
            return JsonResponse({"status": "error", "msg": "您已有预约！"})

        # create a reservation
        reservation_obj = Reservation.objects.create(
            student_id=id,
            seat_id=seat_id,
            start_time=start_time,
            end_time=end_time,
            status=0              #初始为未签到（0）
        )
        reservation_obj.save()

        return JsonResponse({"status": "success", "msg": "预约成功！"})
    else:
        return JsonResponse({"status": "error", "msg": "预约失败！"})

import time
#print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
#print(time.localtime().tm_year) #年
#print(time.localtime().tm_mon) #月
#print(time.localtime().tm_mday) # 获取几号
print(time.localtime().tm_hour)


#再次预约座位
def again_reservation(request):
    
    print("again reservation")  

    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))       #如果获取的数据是none就加一下
        seat_id = data.get('seat_id')
        id = data.get('sid')
        student_obj = Student.objects.get(id=id)             
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        now = data.get('time')      #请求的时间
        
        # transform the time format
        start_time = datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S")          
        end_time = datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%S")
        print(start_time,end_time,start_time.year,now,start_time.month,start_time.day)
        now = datetime.strptime(now, "%Y-%m-%d %H:%M:%S")     #当前的时间
        again_start = start_time.replace(now.year,now.month,now.day)
        again_end = end_time.replace(now.year,now.month,now.day)
        print(again_start,again_end)           #新的预约时间
        #卡这儿了？
        # Check if the person has a reservation
        if Reservation.objects.filter(student_id=id, seat_id=seat_id).exclude(status=3).exists():           #当前座位有预约了,seat_id为seat表的id(_lt这种写法不行)
            print("already has?")
            return JsonResponse({"status": "error", "msg": "您已有预约！"})

        
        '''
        #判断是否约满
        stime = time.strftime("%M", start_time)
        print("start hour:",stime)
        ehour = datetime.strptime(end_time,"%Y-%m-%d %H:%M:%S")          #结束的时间
        etime = ehour.hour

        books = [0]*24       #一天的预定情况        
        res = Reservation.objects.filter(seat_id=seat_id)   #需要获取当天的数据，待补，暂时不考虑不是同一天的情况
        for re in res:
            st = datetime.strptime(re.start_time,"%Y-%m-%d %H:%M:%S")
            sh = st.hour
            et = datetime.strptime(re.end_time,"%Y-%m-%d %H:%M:%S")          #结束的时间
            eh = et.hour
            for i in range(sh,eh):
                books[i] = 1

        cans= -1      #可以预约的最早时间
        cane = etime        #必须结束的时间
        #booked = Booked.objects.filter(seat_id=seat_id)         #获取该座位的预约情况
        for i in range(stime,etime):
            if books[i] == 0:
                #尚未被预约
                cans = i  #增加一个可预约时间
                break
        if cans != -1:     #有部分时间可以约
            for i in range(cans,cane):
                if books[i] == 1 :
                    cane = i
                    break
            t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            h = datetime.strptime(cans,'%H:%M:%S')
            print(t,h)
            print(t.getDate())
            print(t.getDate()+h)
        else:
            return JsonResponse({"status": "error", "msg": "预约失败(当前位置没有空余时间)！"}) 
        # create a reservation
        '''
        reservation_obj = Reservation.objects.create(
            student_id=id,
            seat_id=seat_id,
            start_time=again_start,
            end_time=again_end,
            status=0              #初始为未签到（0）
        )
        reservation_obj.save()

        return JsonResponse({"status": "success", "msg": "预约成功！"})
    else:
        return JsonResponse({"status": "error", "msg": "预约失败！"})   #请求方式不对

import random
#抢座
def get(request):
    
    print("get seat")

    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))       #如果获取的数据是none就加一下
        time = data.get('time')
        id = data.get('sid')
        student_obj = Student.objects.get(id=id)             
        #the_seat = Seat.objects.get(id=room_id, seat_id=seat_id)
        #print(the_seat)
        now = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")     #当前的时间
        #print((datetime.datetime.now()+datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S"))  #多加一天
        #h= (now+datetime.timedelta(hours=2)).strftime("%Y-%m-%d %H")   +":00:00"
        h= now.replace(now.year,now.month,now.day,now.hour+2,0,0)
        print ("next 2 hour=",h)
        # transform the time format
        start_time = now
        end_time = h
        print(start_time,end_time)
        # Check if the person has a reservation
        last = Seat.objects.count() - 1          #总共有多少座位
        print("seat num:",last)
        index = random.randint(0, last)
        print("random num:",index)
        rseat = Seat.objects.all()[index]
        print("rseat",rseat.seat_id)
        seat_id = rseat.seat_id     #座位id

        if Reservation.objects.filter(student=student_obj, seat=rseat).exclude(status=3).exists():           #当前座位有预约了,seat_id为seat表的id
            return JsonResponse({"status": "error", "msg": "您已有预约，抢座失败！"})
       
        # create a reservation
        reservation_obj = Reservation.objects.create(
            student_id=id,
            seat_id=seat_id,
            start_time=start_time,
            end_time=end_time,
            status=0              #初始为未签到（0）
        )
        reservation_obj.save()
        msg = '您成功抢到了'+str(start_time.hour)+':'+str(start_time.minute)+':'+str(start_time.microsecond)+'-'+str(end_time.hour)+':00:00'+'座位号为'+str(seat_id)+'的座位'
        return JsonResponse({"status": "success", "msg": msg})

    else:
        return JsonResponse({"status": "error", "msg": "抢座失败！"})

class ReservationSerializerForStudent(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['id','seat_id', 'start_time', 'end_time', 'status','create_time']

#显示预约情况
def view_reservation(request):
    print("in view reservation")

    #username = request.META.get('HTTP_USERNAME')
    #stu_id = Student.objects.get(name=username).id
    
    
    if request.method == "GET":
        print("method:",request.method)
        #data = json.loads(request.body.decode('utf-8'))       #如果获取的数据是none就加一下
        #sid = data.get('sid')
        sid = request.get('sid')
        print("student id:",sid)
        reservation_query_set = Reservation.objects.filter(student_id=sid)
        
        reservation_serializer = ReservationSerializerForStudent(reservation_query_set, many=True)
        reservation_data = reservation_serializer.data
        return JsonResponse({"reservation_list": reservation_data}, safe=False)

    elif request.method == "POST": 
        data = json.loads(request.body.decode('utf-8'))       #如果获取的数据是none就加一下
        sid = data.get('sid')
        tmethod = data.get('method')
        if tmethod == 'getall':
            print("here????")
            #未过期的数据（当天的数据）
            reservation_query_set = Reservation.objects.filter(student_id=sid).exclude(status=3)
            print('yuyue',reservation_query_set)
            reservation_serializer = ReservationSerializerForStudent(reservation_query_set, many=True)
            reservation_data = reservation_serializer.data
            #历史记录
            hreservation_query_set = Reservation.objects.filter(student_id=sid,status=3)
            print('history',hreservation_query_set)
            hreservation_serializer = ReservationSerializerForStudent(hreservation_query_set, many=True)
            hreservation_data = hreservation_serializer.data

            return JsonResponse({"reservation_list": reservation_data,"history":hreservation_data}, safe=False)
        else:
            reservation_id = request.POST.get('reservation_id')
            reservation_obj = Reservation.objects.get(id=reservation_id)
            reservation_obj.status = 3  # update the status
            reservation_obj.save()
            return JsonResponse({"status": "success", "msg": "取消成功！"})


#显示座位预约情况
def view_time(request):
    print("in view reservation time")

    if request.method == "POST": 
        data = json.loads(request.body.decode('utf-8'))       #如果获取的数据是none就加一下
        time = data.get('time')
        time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
        room_id =data.get('room_id')
        seat_id = data.get('seat_id')
        start_time = time.replace(time.year,time.month,time.day,0,0,0)
        end_time = time.replace(time.year,time.month,time.day,23,59,59)
        print(start_time,end_time)
        reservation_query_set = Reservation.objects.filter(seat_id=seat_id, start_time__gte = start_time,end_time__lte = end_time)
        print('已预约',reservation_query_set)
        reservation_serializer = ReservationSerializerForStudent(reservation_query_set, many=True)
        reservation_data = reservation_serializer.data
        print("reservation_data:",reservation_data)
        times = []
        for re in reservation_data:
            time = re['start_time']
            time = time.replace('T',' ')
            time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
            etime = re['end_time']
            etime = etime.replace('T',' ')
            etime = datetime.strptime(etime, "%Y-%m-%d %H:%M:%S")
            print(time.hour,etime.hour)
            times.append({"begin":time.hour,"end":etime.hour})
        return JsonResponse({"reservation_list": reservation_data,"time":times}, safe=False)


class WarnSerializerForStudent(serializers.ModelSerializer):
    class Meta:
        model = Warn
        fields = ['title', 'text', 'time', 'is_active']

#警告数据
def view_my_warn(request):
    #username = request.META.get('HTTP_USERNAME')
    #stu_id = Student.objects.get(name=username).id
    data = json.loads(request.body.decode('utf-8'))       #如果获取的数据是none就加一下
    sid = data.get('sid')
    print("warn:",sid)
    warn_query_set = Warn.objects.filter(student_id=sid)
    warn_serializer = WarnSerializerForStudent(warn_query_set, many=True)
    warn_data = warn_serializer.data
    return JsonResponse({"warn_list": warn_data}, safe=False)

#签到
def sign(request):
    print("in sign")
    #username = request.META.get('HTTP_USERNAME')
    #student_obj = Student.objects.get(name=username)
    data = json.loads(request.body.decode('utf-8'))       #如果获取的数据是none就加一下
    sid = data.get('sid')
    
    if request.method == "POST":
        cur_time = data.get('time')
        seat_id = data.get('seat_id')
        createtime = data.get('createtime')
        print(cur_time)
        # transform the time format
        #需要增加定位功能(vue中)
        cur_time = datetime.strptime(cur_time, "%Y-%m-%d %H:%M:%S")
        try:
            the_reservation = Reservation.objects.get(student=sid, seat_id=seat_id,create_time = createtime)
            if the_reservation:
                reservation_start_time = the_reservation.start_time
                if the_reservation.status == "1":
                    return JsonResponse({"status": "error", "msg": "签到失败！您已签到！"})
                if reservation_start_time - timedelta(minutes=10) > cur_time:
                    return JsonResponse({"status": "error", "msg": "签到失败！签到时间未到！"})
                if reservation_start_time + timedelta(minutes=5) < cur_time:
                    return JsonResponse({"status": "error", "msg": "签到失败！签到时间已过！"})
                the_reservation.status = 1
                the_reservation.save(update_fields=["status"])
                return JsonResponse({"status": "success", "msg": "签到成功！"})
        except Reservation.DoesNotExist:
            return JsonResponse({"status": "error", "msg": "签到失败！对象不存在！"})

def cancel(request):
    print("cancel")
    data = json.loads(request.body.decode('utf-8'))       #如果获取的数据是none就加一下
    rid = data.get('rid')
    print("rid:",rid)
    Reservation.objects.filter(id=rid).delete()
    return JsonResponse({"status": "success", "msg": "取消成功！"})

def recommend(request):
    """根据用户的历史预定记录，推荐自习室"""
    #username = request.META.get('HTTP_USERNAME')
    #student_obj = Student.objects.get(name=username)
    #the_reservations = Reservation.objects.filter(student=student_obj).order_by('-start_time')
    data = json.loads(request.body.decode('utf-8'))       #如果获取的数据是none就加一下
    sid = data.get('sid')
    the_reservations = Reservation.objects.filter(student_id=sid).order_by('-start_time')
    # order by the seat_id group count
    seat_id_list = [re.seat_id for re in the_reservations]
    # figure out the most frequent seat
    seat_id_count = Counter(seat_id_list)
    seat_id_count = sorted(seat_id_count.items(), key=lambda x: x[1], reverse=True)
    print(seat_id_count)
    #seats = seat_id_count.filter(state = '空闲')
    #print(seats)

    
    
    # figure out the top 3 seat
    topK = 3
    if len(seat_id_count) < 3:
        topK = len(seat_id_count)
    topK_seat_id = [seat_id_count[i][0] for i in range(topK)]

    seat_query_set = Seat.objects.filter(id__in=topK_seat_id)

    #可以考虑增加过滤非空闲座位
    seats = seat_query_set.filter(state = '开放')
    #print(seats)

    seat_serializer = SeatSerializerForStudent(seats, many=True)
    seat_data = seat_serializer.data

    return JsonResponse({"seat_list": seat_data}, safe=False)


