from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render, reverse
from Equipment.models import Equipment
from Activity.models import Activity, Status
from Activity.forms import ActivityForm, StatusForm
from Activity.utils import *
from Teams.models import Teams
from Common.access_decorators_mixins import (Manager_access_required, Supervisor_access_required, Staff_access_required,
                                            ManagerAccessRequiredMixin, SupervisorAccessRequiredMixin, StaffAccessRequiredMixin)
from Common.models import User

# Create your views here.

@login_required
@Manager_access_required
@Supervisor_access_required
@Staff_access_required
def Activity_List(request):
    if request.method == 'GET':
        if request.user.role == 'ADMIN' or request.user.is_superuser:
            activity = Activity.objects.all().distinct()
        else:
            activity = Activity.objects.filter(Q(created_by=request.user)).distinct()
        today =datetime.today().date()
        status = Status.objects.all().distinct()
        return render(request, 'activity_list.html', {'activity':activity, 'status':status, 'source_choices':SOURCE_CHOICES, 'today':today})

    if request.method == 'POST':
        activity = Activity.objects.filter()
        if request.user.role == 'ADMIN' or request.user.is_superuser:
            activity = activity
        else:
            activity = Activity.objects.filter(created_by=request.user)

        if request.POST.get('equipment_name', None):
            eqp = Equipment.objects.get(name__icontains=request.POST.get('equipment_name'))
            activity = activity.filter(equipment_ids=eqp.id)
        if request.POST.get('source', None):
            activity = activity.filter(source=request.POST.get('source'))
        if request.POST.get('status_ids', None):
            activity = activity.filter(status_ids=request.POST.get('status_ids'))
        if request.POST.get('is_active', None):
            activity = activity.filter(is_active=request.POST.get('is_active'))

        activity = activity.distinct()
        today = datetime.today().date()
        status = Status.objects.all().distinct()
        return render(request, 'activity_list.html', {'activity': activity, 'status':status, 'source_choices':SOURCE_CHOICES, 'today':today})


@login_required
@Staff_access_required
def Activity_Create(request):
    if request.method == 'GET':
        if request.user.role == 'ADMIN' or request.user.is_superuser:
            users = User.objects.filter(is_active=True).order_by('username')
        else:
            users = User.objects.filter(role='ADMIN').order_by('username')
        form = ActivityForm(request_user=request.user)
        return render(request, 'activity_create.html', {'form':form, 'users':users})

    if request.method == 'POST':
        form = ActivityForm(request.POST, request_user=request.user)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.created_by = request.user
            activity.save()
            return redirect('Activity:Activity_List')
        else:
            return JsonResponse({'error':True, 'errors': form.errors})


@login_required
@Supervisor_access_required
@Staff_access_required
def Activity_Detail(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)

    if not (request.user.role == 'ADMIN' or request.user.is_superuser or activity.created_by == request.user):
        raise PermissionDenied

    if request.method == 'GET':
        if request.user.is_superuser or request.user.role == 'ADMIN':
            users_mention = list(User.objects.filter(is_active=True).values('username'))
        elif request.user != activity.created_by:
            users_mention = [{'username': activity.created_by.username}]
        else:
            users_mention = list(activity.created_by.all().values('username'))
        return render(request, 'activity_detail.html', {'activity': activity, 'users_mention': users_mention})


@login_required
@Staff_access_required
def Activity_Edit(request, activity_id):
    activity_obj = get_object_or_404(Activity, pk=activity_id)

    if not (request.user.role == 'ADMIN' or request.user.is_superuser or activity_obj.created_by == request_user):
        raise PermissionDenied

    if request.method == 'GET':
        if request.user.role == 'ADMIN' or request.user.is_superuser:
            users = User.objects.filter(is_active=True).order_by('username')
        else:
            users = User.objects.filter(role='ADMIN').order_by('username')
        form = ActivityForm(instance=activity_obj, request_user=request.user)
        return render(request, 'activity_create.html', {'form':form, 'activity_obj':activity_obj, 'users':users})

    if request.method == 'POST':
        form = ActivityForm(request.POST, instance=activity_obj, request_user=request.user)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.updated_on = datetime.today()
            activity.updated_by = request.user
            activity.save()
            return redirect('Activity:Activity_List')
        else:
            return JsonResponse({'error':True, 'errors': form.errors})


@login_required
@Manager_access_required
def Activity_Delete(request, activity_id):
    activity_obj = get_object_or_404(Activity, pk=activity_id)

    if not (request.user.role == 'ADMIN' or request.user.is_superuser or activity_obj.created_by == request.user):
        raise PermissionDenied

    if request.method == 'GET':
        activity_obj.delete()
        return redirect('Activity:Activity_List')

#======================================================================================

@login_required
@Manager_access_required
@Supervisor_access_required
@Staff_access_required
def Status_List(request):
    if request.method == 'GET':
        if request.user.role == 'ADMIN' or request.user.is_superuser:
            status = Status.objects.all().distinct()
        else:
            status = Status.objects.filter(Q(created_by=request.user)).distinct()
        today =datetime.today().date()
        return render(request, 'status_list.html', {'status':status, 'today':today})

    if request.method == 'POST':
        status = Status.objects.filter()
        if request.user.role == 'ADMIN' or request.user.is_superuser:
            status = status
        else:
            status = Status.objects.filter(created_by=request.user)

        if request.POST.get('name', None):
            status = status.filter(name__icontains=request.POST.get('name'))
        if request.POST.get('is_active', None):
            status = status.filter(is_active=request.POST.get('is_active'))

        status = status.distinct()
        today = datetime.today().date()
        return render(request, 'status_list.html', {'status':status,'today':today})


@login_required
@Staff_access_required
def Status_Create(request):
    if request.method == 'GET':
        if request.user.role == 'ADMIN' or request.user.is_superuser:
            users = User.objects.filter(is_active=True).order_by('username')
        else:
            users = User.objects.filter(role='ADMIN').order_by('username')
        form = StatusForm(request_user=request.user)
        return render(request, 'status_create.html', {'form':form, 'users':users})

    if request.method == 'POST':
        form = StatusForm(request.POST, request_user=request.user)
        if form.is_valid():
            status = form.save(commit=False)
            status.created_by = request.user
            status.save()
            return redirect('Activity:Status_List')
        else:
            return JsonResponse({'error':True, 'errors': form.errors})


@login_required
@Supervisor_access_required
@Staff_access_required
def Status_Detail(request, status_id):
    status = get_object_or_404(Status, pk=status_id)

    if not (request.user.role == 'ADMIN' or request.user.is_superuser or status.created_by == request.user):
        raise PermissionDenied

    if request.method == 'GET':
        if request.user.is_superuser or request.user.role == 'ADMIN':
            users_mention = list(User.objects.filter(is_active=True).values('username'))
        elif request.user != status.created_by:
            users_mention = [{'username': status.created_by.username}]
        else:
            users_mention = list(status.created_by.all().values('username'))
        return render(request, 'status_detail.html', {'status': status, 'users_mention': users_mention})


@login_required
@Staff_access_required
def Status_Edit(request, status_id):
    status_obj = get_object_or_404(Status, pk=status_id)

    if not (request.user.role == 'ADMIN' or request.user.is_superuser or status_obj.created_by == request_user):
        raise PermissionDenied

    if request.method == 'GET':
        if request.user.role == 'ADMIN' or request.user.is_superuser:
            users = User.objects.filter(is_active=True).order_by('username')
        else:
            users = User.objects.filter(role='ADMIN').order_by('username')
        form = StatusForm(instance=status_obj, request_user=request.user)
        return render(request, 'status_create.html', {'form':form, 'status_obj':status_obj, 'users':users})

    if request.method == 'POST':
        form = StatusForm(request.POST, instance=status_obj, request_user=request.user)
        if form.is_valid():
            status = form.save(commit=False)
            status.updated_on = datetime.today()
            status.updated_by = request.user
            status.save()
            return redirect('Activity:Status_List')
        else:
            return JsonResponse({'error':True, 'errors': form.errors})


@login_required
@Manager_access_required
def Status_Delete(request, status_id):
    status_obj = get_object_or_404(Status, pk=status_id)

    if not (request.user.role == 'ADMIN' or request.user.is_superuser or status_obj.created_by == request.user):
        raise PermissionDenied

    if request.method == 'GET':
        status_obj.delete()
        return redirect('Activity:Status_List')
