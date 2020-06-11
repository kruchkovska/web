from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect, HttpResponseBadRequest
from django.urls import reverse

from .models import student, Perevod

def index(request):
    student_info = student.objects.all()
    return render(request, 'student/list.html', {'student_info': student_info})

def detail(request,student_id):
    try:
        a = Student.objects.get(id = student_id)
    except:
        raise Http404("Student doesn`t exist :(")

    latest_perevod_list = a.perevod_set.order_by('-id')[:3] 


    return render(request, 'student/detail.html', {'student': a, 'latest_perevod_list': latest_perevod_list})

def make_transaction(request,student_id):
    try:
        a = student.objects.get(id = student_id)
    except:
        raise Http404("student doesn`t exist, Sir :(")
    check = int(request.POST['text'])



    a.perevod_set.create(user_name = request.POST['name'],user_perevod = request.POST['text'])
    emount = int(request.POST['text'])

    if request.POST['name'] == a.student_name and request.POST['receiver'] == a.father_name:
        a.father_rate += emount
        a.student_rate -= emount
        a.save()
    elif request.POST['name'] == a.father_name and request.POST['receiver'] == a.student_name:
        a.student_rate += emount
        a.father_rate -= emount
        a.save()

    if request.POST['name'] == a.student_name and request.POST['receiver'] == a.mother_name:
        a.mother_rate += emount
        a.student_rate -= emount
        a.save()
    elif request.POST['name'] == a.mother_name and request.POST['receiver'] == a.student_name:
        a.student_rate += emount
        a.mother_rate -= emount
        a.save()    

    if request.POST['name'] == a.student_name and request.POST['receiver'] == a.child_name:
        a.child_rate += emount
        a.student_rate -= emount
        a.save() 
    elif request.POST['name'] == a.child_name and request.POST['receiver'] == a.student_name:
        a.student_rate += emount
        a.child_rate -= emount
        a.save()
       
    #a.student_rate += emount
    #a.save()

    return HttpResponseRedirect(reverse('student:detail', args=(a.id,)))
