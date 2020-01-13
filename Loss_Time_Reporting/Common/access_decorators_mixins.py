from functools import wraps

from django.contrib.auth.mixins import AccessMixin, LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect

def admin_access_required(functions):

    def wraps(request, *args, **kwargs):
        if request.user.role =='ADMIN' or request.user.is_superuser or request.user.is_admin:
            return functions(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wraps

def Manager_access_required(functions):

    def wraps(request, *args, **kwargs):
        if request.user.role =='ADMIN' or request.user.is_superuser or request.user.has_manager_access:
            return functions(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wraps

def Supervisor_access_required(functions):

    def wraps(request, *args, **kwargs):
        if request.user.role =='ADMIN' or request.user.is_superuser or request.user.has_supervisor_access:
            return functions(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wraps

def Staff_access_required(functions):

    def wraps(request, *args, **kwargs):
        if request.user.role =='ADMIN' or request.user.is_superuser or request.user.has_staff_access:
            return functions(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wraps

class AdminRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        self.raise_exception = True
        if not request.user.role == "ADMIN":
            if not request.user.is_superuser:
                return self.handle_no_permission()
        return super(AdminRequiredMixin, self).dispatch(
            request, *args, **kwargs)

class ManagerAccessRequiredMixin(AccessMixin):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        self.raise_exception = True
        if request.user.role == 'ADMIN' or request.user.is_superuser or request.user.has_manager_access:
            return super(ManagerAccessRequiredMixin, self).dispatch(request, *args, *kwargs)
        else:
            return self.handle_no_permission()

class SupervisorAccessRequiredMixin(AccessMixin):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        self.raise_exception = True
        if request.user.role == 'ADMIN' or request.user.is_superuser or request.user.has_manager_access:
            return super(ManagerAccessRequiredMixin, self).dispatch(request, *args, *kwargs)
        else:
            return self.handle_no_permission()

class StaffAccessRequiredMixin(AccessMixin):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        self.raise_exception = True
        if request.user.role == 'ADMIN' or request.user.is_superuser or request.user.has_manager_access:
            return super(ManagerAccessRequiredMixin, self).dispatch(request, *args, *kwargs)
        else:
            return self.handle_no_permission()
