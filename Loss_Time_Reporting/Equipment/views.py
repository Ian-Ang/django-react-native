from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render, reverse
#from django.views.generic import (CreateView, DeleteView, DetailView, FormView, TemplateView, UpdateView, View)

from Equipment.models import Equipment, Locate
from Equipment.forms import EquipmentForm, LocateForm
from Teams.models import Teams
from Common.access_decorators_mixins import (Manager_access_required, Supervisor_access_required, Staff_access_required,
                                            ManagerAccessRequiredMixin, SupervisorAccessRequiredMixin, StaffAccessRequiredMixin)
from Common.models import User

# Create your views here.

@login_required
@Manager_access_required
@Supervisor_access_required
@Staff_access_required
def Equipment_List(request):
    if request.method == 'GET':

        if request.user.role == 'ADMIN' or request.user.is_superuser:
            equipment = Equipment.objects.all().distinct()
        else:
            equipment = Equipment.objects.filter(Q(created_by=request.user)).distinct()
        today =datetime.today().date()
        locate = Locate.objects.all().distinct()
        return render(request, 'equipment_list.html', {'equipment':equipment, 'locate':locate, 'today':today})

    if request.method == 'POST':
        equipment = Equipment.objects.filter()
        if request.user.role == 'ADMIN' or request.user.is_superuser:
            equipment = equipment
        else:
            equipment = Equipment.objects.filter(created_by=request.user)

        if request.POST.get('locate_id', None):
            equipment = equipment.filter(locate_id=request.POST.get('locate_id'))
        if request.POST.get('equipment_name', None):
            equipment = equipment.filter(name__icontains=request.POST.get('equipment_name'))
        if request.POST.get('qr_code', None):
            equipment = equipment.filter(qr_code=request.POST.get('qr_code'))
        if request.POST.get('is_active', None):
            equipment = equipment.filter(is_active=request.POST.get('is_active'))

        equipment = equipment.distinct()

        today = datetime.today().date()
        return render(request, 'equipment_list.html', {'equipment': equipment, 'today':today})

@login_required
@Staff_access_required
def Equipment_Create(request):
    if request.method == 'GET':
        if request.user.role == 'ADMIN' or request.user.is_superuser:
            users = User.objects.filter(is_active=True).order_by('username')
        else:
            users = User.objects.filter(role='ADMIN').order_by('username')
        form = EquipmentForm(request_user=request.user)
        return render(request, 'equipment_create.html', {'form':form, 'users':users})

    if request.method == 'POST':
        form = EquipmentForm(request.POST, request_user=request.user)
        if form.is_valid():
            equipment = form.save(commit=False)
            equipment.created_by = request.user
            equipment.save()

            #if request.POST.getlist('teams', []):
                #user_ids = Teams.objects.filter(id__in=request.POST.getlist('teams')).values_list('users', flat=True)
                #assigned_to_user_ids = Equipment.assigned_to.all().values_list('id', flat=True)
                #for user_id in user_ids:
                #    if user_id not in assigned_to_user_ids:
                #        equipment.assigned_to.add(user_id)

            #kwargs = {'domain': request.get_host(), 'protocol': request.scheme}
            #send_email.delay(equipment.id, **kwargs)
            #success_url = reverse('Equipment:Equipment_List')
            #if request.POST.get('from_Locate_id'):
                #success_url = reverse('Equipment:view_locate', args=(request.POST.get('from_Locate_id'),))
            #return JsonResponse({'error': False, 'success_url':success_url})
            return redirect('Equipment:Equipment_List')
        else:
            return JsonResponse({'error':True, 'errors': form.errors})

@login_required
@Supervisor_access_required
@Staff_access_required
def Equipment_Detail(request, equipment_id):
    equipment = get_object_or_404(Equipment, pk=equipment_id)

    if not (request.user.role == 'ADMIN' or request.user.is_superuser or equipment.created_by == request.user):
        raise PermissionDenied

    if request.method == 'GET':
        if request.user.is_superuser or request.user.role == 'ADMIN':
            users_mention = list(User.objects.filter(is_active=True).values('username'))
        elif request.user != equipment.created_by:
            users_mention = [{'username': equipment.created_by.username}]
        else:
            users_mention = list(equipment.created_by.all().values('username'))
        return render(request, 'equipment_detail.html', {'equipment': equipment, 'users_mention': users_mention})

@login_required
@Staff_access_required
def Equipment_Edit(request, equipment_id):
    equipment_obj = get_object_or_404(Equipment, pk=equipment_id)

    if not (request.user.role == 'ADMIN' or request.user.is_superuser or equipment_obj.created_by == request_user):
        raise PermissionDenied

    if request.method == 'GET':
        if request.user.role == 'ADMIN' or request.user.is_superuser:
            users = User.objects.filter(is_active=True).order_by('username')
        else:
            users = User.objects.filter(role='ADMIN').order_by('username')
        form = EquipmentForm(instance=equipment_obj, request_user=request.user)
        return render(request, 'equipment_create.html', {'form':form, 'equipment_obj':equipment_obj, 'users':users})

    if request.method == 'POST':
        form = EquipmentForm(request.POST, instance=equipment_obj, request_user=request.user)
        if form.is_valid():
            equipment = form.save(commit=False)
            equipment.updated_by = request.user
            equipment.save()
            #form.save_m2m()

            #if request.POST.getlist('teams', []):
                #user_ids = Teams.objects.filter(id__in=request.POST.getlist('teams')).values_list('users', flat=True)
                #assigned_to_user_ids = Equipment.assigned_to.all().values_list('id', flat=True)
                #for user_id in user_ids:
                #    if user_id not in assigned_to_user_ids:
                #        equipment.assigned_to.add(user_id)

            #kwargs = {'domain': request.get_host(), 'protocol': request.scheme}
            #send_email.delay(equipment.id, **kwargs)
            #success_url = reverse('Equipment:Equipment_List')
            #if request.POST.get('from_Locate_id'):
                #success_url = reverse('Equipment:view_locate', args=(request.POST.get('from_Locate_id'),))
            #return JsonResponse({'error': False, 'success_url':success_url})
            return redirect('Equipment:Equipment_List')
        else:
            return JsonResponse({'error':True, 'errors': form.errors})

@login_required
@Manager_access_required
def Equipment_Delete(request, equipment_id):
    equipment_obj = get_object_or_404(Equipment, pk=equipment_id)

    if not (request.user.role == 'ADMIN' or request.user.is_superuser or equipment_obj.created_by == request.user):
        raise PermissionDenied

    if request.method == 'GET':
        equipment_obj.delete()

        #if request.GET.get('view_locate', None):
        #    return redirect(reverse('Equipment:view_locate', args=(request.GET.get('view_locate'),)))
        return redirect('Equipment:Equipment_List')

"""========================================================="""

@login_required
@Manager_access_required
@Supervisor_access_required
@Staff_access_required
def Locate_List(request):
    if request.method == 'GET':

        if request.user.role == 'ADMIN' or request.user.is_superuser:
            locate = Locate.objects.all().distinct()
        else:
            locate = Locate.objects.filter(Q(created_by=request.user)).distinct()
        today =datetime.today().date()
        return render(request, 'locate_list.html', {'locate':locate, 'today':today})

    if request.method == 'POST':
        locate = Locate.objects.filter()
        if request.user.role == 'ADMIN' or request.user.is_superuser:
            locate = locate
        else:
            locate = Locate.objects.filter(created_by=request.user)


        if request.POST.get('name', None):
            locate = locate.filter(name=request.POST.get('name'))
        if request.POST.get('is_active', None):
            locate = locate.filter(is_active=request.POST.get('is_active'))

        locate = locate.distinct()

        today = datetime.today().date()
        return render(request, 'locate_list.html', {'locate': locate, 'today':today})

@login_required
@Staff_access_required
def Locate_Create(request):
    if request.method == 'GET':
        if request.user.role == 'ADMIN' or request.user.is_superuser:
            users = User.objects.filter(is_active=True).order_by('username')
        else:
            users = User.objects.filter(role='ADMIN').order_by('username')
        form = LocateForm(request_user=request.user)
        return render(request, 'locate_create.html', {'form':form, 'users':users})

    if request.method == 'POST':
        form = LocateForm(request.POST, request_user=request.user)
        if form.is_valid():
            #locate.id =
            locate = form.save(commit=False)
            locate.created_by = request.user
            locate.save()

            #if request.POST.getlist('teams', []):
                #user_ids = Teams.objects.filter(id__in=request.POST.getlist('teams')).values_list('users', flat=True)
                #assigned_to_user_ids = Equipment.assigned_to.all().values_list('id', flat=True)
                #for user_id in user_ids:
                #    if user_id not in assigned_to_user_ids:
                #        equipment.assigned_to.add(user_id)

            #kwargs = {'domain': request.get_host(), 'protocol': request.scheme}
            #send_email.delay(equipment.id, **kwargs)
            #success_url = reverse('Equipment:Locate_List')
            #if request.POST.get('from_Locate_id'):
            #    success_url = reverse('Equipment:view_locate', args=(request.POST.get('from_Locate_id'),))
            #return JsonResponse({'error': False, 'success_url':success_url})
            return redirect('Equipment:Locate_List')
        else:
            return JsonResponse({'errors': form.errors})


@login_required
@Supervisor_access_required
@Staff_access_required
def Locate_Detail(request, locate_id):
    locate = get_object_or_404(Locate, pk=locate_id)

    if not (request.user.role == 'ADMIN' or request.user.is_superuser or equipment.created_by == request.user):
        raise PermissionDenied

    if request.method == 'GET':
        if request.user.is_superuser or request.user.role == 'ADMIN':
            users_mention = list(User.objects.filter(is_active=True).values('username'))
        elif request.user != locate.created_by:
            users_mention = [{'username': locate.created_by.username}]
        else:
            users_mention = list(locate.created_by.all().values('username'))
        return render(request, 'locate_detail.html', {'locate': locate, 'users_mention': users_mention})


@login_required
@Staff_access_required
def Locate_Edit(request, locate_id):
    locate_obj = get_object_or_404(Locate, pk=locate_id)

    if not (request.user.role == 'ADMIN' or request.user.is_superuser or equipment_obj.created_by == request_user):
        raise PermissionDenied

    if request.method == 'GET':
        if request.user.role == 'ADMIN' or request.user.is_superuser:
            users = User.objects.filter(is_active=True).order_by('username')
        else:
            users = User.objects.filter(role='ADMIN').order_by('username')
        form = LocateForm(instance=locate_obj, request_user=request.user)
        return render(request, 'locate_create.html', {'form':form, 'locate_obj':locate_obj, 'users':users})

    if request.method == 'POST':
        form = LocateForm(request.POST, instance=locate_obj, request_user=request.user)
        if form.is_valid():
            locate = form.save(commit=False)
            locate.updated_by = request.user
            locate.save()
            #form.save_m2m()

            #if request.POST.getlist('teams', []):
                #user_ids = Teams.objects.filter(id__in=request.POST.getlist('teams')).values_list('users', flat=True)
                #assigned_to_user_ids = Equipment.assigned_to.all().values_list('id', flat=True)
                #for user_id in user_ids:
                #    if user_id not in assigned_to_user_ids:
                #        equipment.assigned_to.add(user_id)

            #kwargs = {'domain': request.get_host(), 'protocol': request.scheme}
            #send_email.delay(equipment.id, **kwargs)
            #success_url = reverse('Equipment:Equipment_List')
            #if request.POST.get('from_Locate_id'):
                #success_url = reverse('Equipment:view_locate', args=(request.POST.get('from_Locate_id'),))
            #return JsonResponse({'error': False, 'success_url':success_url})
            return redirect('Equipment:Locate_List')
        else:
            return JsonResponse({'errors': form.errors})

@login_required
@Manager_access_required
def Locate_Delete(request, locate_id):
    locate_obj = get_object_or_404(Locate, pk=locate_id)

    if not (request.user.role == 'ADMIN' or request.user.is_superuser or equipment_obj.created_by == request.user):
        raise PermissionDenied

    if request.method == 'GET':
        locate_obj.delete()

        #if request.GET.get('view_locate', None):
            #return redirect(reverse('Equipment:view_locate', args=(request.GET.get('view_locate'),)))
        return redirect('Equipment:Locate_List')
