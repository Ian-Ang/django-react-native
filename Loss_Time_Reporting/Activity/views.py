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
from Activity.forms import ActivityForm
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
        return render(request, 'activity_list.html', {'activity':activity, 'status':status, 'today':today})

    if request.method == 'POST':
        activity = Activity.objects.filter()
        if request.user.role == 'ADMIN' or request.user.is_superuser:
            activity = activity
        else:
            activity = Activity.objects.filter(created_by=request.user)

        if request.POST.get('equipment_ids', None):
            activity = Activity.filter(equipment_ids=request.POST.get('equipment_ids'))
        if request.POST.get('source', None):
            activity = Activity.filter(source__icontains=request.POST.get('source'))
        if request.POST.get('status_ids', None):
            activity = Activity.filter(status_ids=request.POST.get('status_ids'))
        if request.POST.get('is_active', None):
            activity = Activity.filter(is_active=request.POST.get('is_active'))

        activity = activity.distinct()

        today = datetime.today().date()
        return render(request, 'activity_list.html', {'activity': activity, 'today':today})
