import os
import json
import datetime
from django.conf import settings
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (CreateView, UpdateView, DetailView, TemplateView, View, DeleteView)
from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse, Http404
from django.urls import reverse_lazy, reverse
from django.template.loader import render_to_string
from django.core.exceptions import PermissionDenied
from django.utils import timezone
from Common.access_decorators_mixins import (
            admin_access_required, Manager_access_required, Supervisor_access_required, Staff_access_required,
            AdminRequiredMixin, ManagerAccessRequiredMixin, SupervisorAccessRequiredMixin, StaffAccessRequiredMixin)
from Activity.models import Activity
from Equipment.models import Equipment
from Common.utils import ROLES
from Common.forms import UserForm, LoginForm, ChangePasswordForm
from Common.models import User

def handler404(request, exception):
    return render(request, '404.html', status=404)

def handler500(request):
    return render(request, '500.html', status=500)

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        activity = Activity.objects.all()
        equipment = Equipment.objects.all()
        if self.request.user.role == "ADMIN" or self.request.user.is_superuser:
            pass
        else:
            activity = Activity.filter(Q(create_by=self.request.user.id))
            equipment = Equipment.filter(Q(create_by=self.request.user.id))
        context["activitys"] = activity
        context["equipments"] = equipment
        return context

class ChangePasswordView(LoginRequiredMixin, TemplateView):
    template_name = "change_password.html"

    def get_context_data(self, **kwargs):
        context = super(ChangePasswordView, self).get_context_data(**kwargs)
        context["change_password_form"] = ChangePasswordForm()
        return context

    def post(self, request, *args, **kwargs):
        error, errors = "", ""
        form = ChangePasswordForm(request.POST, user=request.user)
        if form.is_valid():
            user = request.user
            # if not check_password(request.POST.get('CurrentPassword'),
            #                       user.password):
            #     error = "Invalid old password"
            # else:
            user.set_password(request.POST.get('Newpassword'))
            user.is_active = True
            user.save()
            return HttpResponseRedirect('/')
        else:
            errors = form.errors
        return render(request, "change_password.html",
                      {'error': error, 'errors': errors,'change_password_form': form})

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "profile.html"

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context["user_obj"] =  self.request.user
        return context

class LoginView(TemplateView):
    template_name = "login.html"

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        return context

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/')
        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST, request=request)
        if form.is_valid():

            user = User.objects.filter(username=request.POST.get('username')).first()
            # user = authenticate(username=request.POST.get('email'), password=request.POST.get('password'))
            if user is not None:
                if user.is_active:
                    user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))

                    if user is not None:
                        login(request, user)
                        if user.has_manager_access:
                            return HttpResponseRedirect('/')
                        elif user.has_supervisor_access:
                            return HttpResponseRedirect('/') #return redirect('marketing:dashboard')
                        elif user.has_staff_access:
                            return HttpResponseRedirect('/')
                        else :
                            return HttpResponseRedirect('/')
                    return render(request, "login.html", {
                        "error": True,
                        "messages":"Your username and password didn't match. Please try again."})
                return render(request, "login.html", {
                    "error": True,
                    "messages":"Your Account is inactive. Please Contact Administrator"})
            return render(request, "login.html", {
                "error": True,
                "messages":"Your Account is not Found. Please Contact Administrator"})

        return render(request, "login.html", {
            # "error": True,
            # "messages": "Your username and password didn't match. Please try again."
            "form": form
        })

class ForgotPasswordView():
    template_name = "forgot_password.html"


class LogoutView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        logout(request)
        request.session.flush()
        return redirect("Common:login")

class UserListView(AdminRequiredMixin, TemplateView):
    model = User
    context_object_name = "users"
    template_name = "list.html"

    def get_queryset(self):
        queryset = self.model.objects.all()

        request_post = self.request.POST
        if request_post:
            if request_post.get('username'):
                queryset = queryset.filter(username__incotains=request_post.get('username'))
            if request_post.get('email'):
                queryset = queryset.filter(email__incotains=request_post.get('email'))
            if request_post.get('role'):
                queryset = queryset.filter(role=request_post.get('role'))

        return queryset.order_by('username')

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        active_users = self.get_queryset().filter(is_active=True)
        inactive_users = self.get_queryset().filter(is_active=False)
        context["active_users"] = active_users
        context["inactive_users"] = inactive_users
        context["per_page"] = self.request.POST.get('per_page')
        context['admin_email'] = settings.ADMIN_EMAIL
        context['role'] = ROLES
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_string(context)

class CreateUserView(AdminRequiredMixin, CreateView):
    model = User
    form_class = UserForm
    template_name = "create.html"

    pass
