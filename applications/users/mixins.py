from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy

from .models import User


class AdministradorPermisoMixin(LoginRequiredMixin):
    login_url = reverse_lazy('app_users:login')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if request.user.occupation != User.ADMINISTRADOR and not request.user.is_superuser:
            return HttpResponseRedirect(reverse('app_users:login'))
        return super().dispatch(request, *args, **kwargs)


class VentasPermisoMixin(LoginRequiredMixin):
    login_url = reverse_lazy('app_users:login')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if request.user.occupation not in [User.ADMINISTRADOR, User.VENTAS] and not request.user.is_superuser:
            return HttpResponseRedirect(reverse('app_users:login'))
        return super().dispatch(request, *args, **kwargs)


class ClientePermisoMixin(LoginRequiredMixin):
    login_url = reverse_lazy('app_users:login')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if request.user.occupation not in [User.ADMINISTRADOR, User.VENTAS, User.CLIENTE] and not request.user.is_superuser:
            return HttpResponseRedirect(reverse('app_users:login'))
        return super().dispatch(request, *args, **kwargs)
