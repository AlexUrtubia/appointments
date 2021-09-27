from django.shortcuts import render, redirect
from .models import *
from login.models import *
from django.contrib import messages
from datetime import date, datetime
# Create your views here.

def appointments(request):
    if 'user_id' not in request.session:
        return redirect('/')
    today = datetime.now()

    context = {
        'active_user': User.objects.get(id=request.session['user_id']),
        'appoint_list': Appointment.objects.filter(user__id = request.session['user_id']).filter(date__gte = today).order_by('date'),
        'past_appo_list': Appointment.objects.filter(user__id = request.session['user_id']).filter(date__lte = today).order_by('date'),
    }
    return render(request, 'appointments.html', context)


def add_appointment(request):
    return render(request, 'add_appo.html')


def new_appo(request):
    active_user = User.objects.get(id=request.session['user_id'])
    errors = {}
    today = datetime.now()
    comp_date = request.POST['date']
    date_object = datetime.strptime(comp_date, "%Y-%m-%d")
    # print("********************","desde formulario:",comp_date,"fecha actual de datetime",today,"Fecha convertida",date_object)

    if len(request.POST['name']) == 0:
        errors['name'] = "Must give a name to your task"
    if request.POST['status'] == '0':
        errors['no_status'] = "Must select a status"
    if len(request.POST['date']) == 0:
        errors['no_date'] = "Must provide a date"
    if today > date_object and request.POST['status'] == 'Pending':
        errors['dates'] = "Future appointments cannot be in set in a past date"
    if len(errors) > 0:
            for key, msg in errors.items():
                messages.error(request, msg)
            return redirect('/appointments/add')
    else:
        Appointment.objects.create(
            name = request.POST['name'],
            status=request.POST['status'],
            date = comp_date,
            user = active_user,
        )
        return redirect('appointments')


def del_appo(request, appo_id):
    appo = Appointment.objects.get(id=appo_id)
    appo.delete()
    return redirect('/appointments')


def edit_appo(request, appo_id):
    context = {
        'appo': Appointment.objects.get(id=appo_id),
        'appo_past': Appointment.objects.get(id=appo_id)
    }
    return render(request, 'edit_appo.html', context)

def upd_appo(request, appo_id):
    errors = {}
    today = datetime.now()
    comp_date = request.POST['date']
    date_object = datetime.strptime(comp_date, "%Y-%m-%d")
    #print("********************","desde formulario:",comp_date,"fecha actual de datetime",today,"Fecha convertida",date_object)
    if len(request.POST['name']) == 0:
        errors['ed_name'] = "Must give a name to your task"
    if request.POST['status'] == '0':
        errors['ed_no_status'] = "Must select a status"
    if len(request.POST['date']) == 0:
        errors['ed_no_date'] = "Must provide a date"
    if today > date_object and request.POST['status'] == 'Pending':
        errors['ed_dates'] = "Future appointments cannot be in set in a past date"
    if len(errors) > 0:
            for key, msg in errors.items():
                messages.error(request, msg)
            return redirect(f'/appointments/{appo_id}/edit')
    else:
        appo = Appointment.objects.get(id=appo_id)
        appo.name = request.POST['name']
        appo.date = request.POST['date']
        appo.status = request.POST['status']
        appo.save()
        return redirect('/appointments')