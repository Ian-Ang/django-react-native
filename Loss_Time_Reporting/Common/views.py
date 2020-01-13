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
            admin_site_required, Manager_required, Supervisor_required, Staff_required,
            AdminRequiredMixin, ManagerAccessRequiredMixin, SupervisorAccessRequiredMixin, StaffAccessRequiredMixin)

from Common.utils import ROLES
from Common.forms import UserForm, LoginForm, ChangePasswordForm
from Common.models import User

def handler404(request, exception):
    return render(request, '404.html', status=404)

def handler500(request):
    return render(request, '500.html', status=500)

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "index.html"

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

class LogoutView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        logout(request)
        request.session.flush()
        return redirect("Common:login")
