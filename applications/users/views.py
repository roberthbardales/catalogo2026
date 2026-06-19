from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, TemplateView, View
from django.views.generic.edit import FormView

from .forms import LoginForm, ResetPasswordForm, UpdatePasswordForm, UserRegisterForm, UserUpdateForm
from .mixins import AdministradorPermisoMixin, VentasPermisoMixin
from .models import User
from applications.products.models import Product, Category, Brand
from applications.quotations.models import QuotationRequest


# --- Helper reutilizable ---
def _es_admin(user):
    return user.is_authenticated and (
        user.is_superuser or user.occupation == User.ADMINISTRADOR
    )


class UserRegisterView(FormView):
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('app_users:login')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['is_admin_context'] = _es_admin(self.request.user)
        return kwargs

    def form_valid(self, form):
        occupation = (
            form.cleaned_data.get('occupation')
            if _es_admin(self.request.user)
            else User.CLIENTE
        )
        User.objects.create_user(
            form.cleaned_data['email'],
            form.cleaned_data['password1'],
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name'],
            occupation=occupation,
            gender=form.cleaned_data['gender'],
            date_birth=form.cleaned_data['date_birth'],
            phone=form.cleaned_data.get('phone', ''),
        )
        return super().form_valid(form)


class LoginUser(FormView):
    template_name = 'users/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('app_users:perfil')

    def form_valid(self, form):
        user = authenticate(
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password']
        )
        if user is None:
            form.add_error(None, 'Email o contraseña incorrectos.')
            return self.form_invalid(form)
        login(self.request, user)
        return super().form_valid(form)


class LogoutView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('app_users:login'))


class UpdatePasswordView(AdministradorPermisoMixin, FormView):
    template_name = 'users/cambiar_password.html'
    form_class = UpdatePasswordForm
    success_url = reverse_lazy('app_users:login')
    login_url = reverse_lazy('app_users:login')

    def form_valid(self, form):
        usuario = self.request.user
        if not usuario.check_password(form.cleaned_data['current_password']):
            form.add_error(None, 'La contraseña actual es incorrecta.')
            return self.form_invalid(form)

        usuario.set_password(form.cleaned_data['new_password'])
        usuario.save()
        logout(self.request)
        return super().form_valid(form)


class DashboardView(VentasPermisoMixin, TemplateView):
    template_name = 'users/dashboard.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['total_products'] = Product.objects.filter(is_active=True).count()
        ctx['total_categories'] = Category.objects.filter(is_active=True).count()
        ctx['total_brands'] = Brand.objects.filter(is_active=True).count()
        ctx['total_quotations'] = QuotationRequest.objects.count()
        ctx['low_stock'] = Product.objects.filter(is_active=True, stock__lt=5, stock__gt=0).count()
        ctx['out_of_stock'] = Product.objects.filter(is_active=True, stock=0).count()
        ctx['recent_quotations'] = QuotationRequest.objects.order_by('-created')[:5]
        ctx['low_stock_products'] = Product.objects.filter(is_active=True, stock__lt=5).select_related('category', 'brand').order_by('stock')[:10]
        return ctx


class PerfilView(LoginRequiredMixin, TemplateView):
    template_name = 'users/perfil.html'
    login_url = reverse_lazy('app_users:login')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['user'] = self.request.user
        ctx['products'] = Product.objects.select_related('category', 'brand').prefetch_related('tags').order_by('name')[:10]
        return ctx


class UserListView(AdministradorPermisoMixin, ListView):
    template_name = 'users/lista_usuarios.html'
    context_object_name = 'usuarios'

    def get_queryset(self):
        qs = User.objects.all()
        if self.request.user.is_superuser:
            return qs.filter(occupation=User.ADMINISTRADOR).order_by('first_name', 'last_name')
        return qs.filter(is_superuser=False).exclude(
            occupation=User.ADMINISTRADOR
        ).order_by('first_name', 'last_name')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['can_create_user'] = (
            self.request.user.occupation == User.ADMINISTRADOR
            and not self.request.user.is_superuser
        )
        return ctx


class UserUpdateView(AdministradorPermisoMixin, FormView):
    template_name = 'users/editar_usuario.html'
    form_class = UserUpdateForm
    success_url = reverse_lazy('app_users:user-list')

    def dispatch(self, request, *args, **kwargs):
        self.usuario = get_object_or_404(User, pk=kwargs['user_id'])
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['is_admin_context'] = _es_admin(self.request.user)
        kwargs['user_instance'] = self.usuario
        kwargs['initial'] = {
            'email':      self.usuario.email,
            'first_name': self.usuario.first_name,
            'last_name':  self.usuario.last_name,
            'occupation': self.usuario.occupation,
            'gender':     self.usuario.gender,
            'phone':      self.usuario.phone,
            'date_birth': self.usuario.date_birth,
        }
        return kwargs

    def form_valid(self, form):
        self.usuario.email      = form.cleaned_data['email']
        self.usuario.first_name = form.cleaned_data['first_name']
        self.usuario.last_name  = form.cleaned_data['last_name']
        self.usuario.gender     = form.cleaned_data['gender']
        self.usuario.phone      = form.cleaned_data.get('phone', '')
        self.usuario.date_birth = form.cleaned_data.get('date_birth')

        if _es_admin(self.request.user) and 'occupation' in form.cleaned_data:
            self.usuario.occupation = form.cleaned_data['occupation']

        self.usuario.save()
        return super().form_valid(form)


class AdminResetPasswordView(AdministradorPermisoMixin, FormView):
    template_name = 'users/reset_password.html'
    form_class = ResetPasswordForm
    success_url = reverse_lazy('app_users:user-list')

    def dispatch(self, request, *args, **kwargs):
        self.usuario = get_object_or_404(User, pk=kwargs['user_id'])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['usuario'] = self.usuario
        return ctx

    def form_valid(self, form):
        self.usuario.set_password(form.cleaned_data['new_password'])
        self.usuario.save()
        return super().form_valid(form)


class ToggleUserActiveView(AdministradorPermisoMixin, View):
    def post(self, request, user_id):
        usuario = get_object_or_404(User, pk=user_id)
        if usuario != request.user:
            usuario.is_active = not usuario.is_active
            usuario.save(update_fields=['is_active'])
        return HttpResponseRedirect(reverse('app_users:user-list'))
