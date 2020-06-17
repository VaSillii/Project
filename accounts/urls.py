from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy
from .views import RegistrationFormView, CustomPasswordChangeView, profile_view, profile_detail

app_name = "accounts"

urlpatterns = [
    path('', profile_view, name='profile_info'),
    path('detail/<int:user_id>/', profile_detail, name='profile_detail'),

    path('auth/login/',
         auth_views.LoginView.as_view(template_name='registration/login.html', redirect_authenticated_user=True),
         name='login'),
    path('auth/logout/', auth_views.LogoutView.as_view(template_name='registration/login.html', next_page='/'),
         name='logout'),
    path('auth/registration/', RegistrationFormView.as_view(template_name='registration/registration.html',
                                                            success_url=reverse_lazy('accounts:login')),
         name='register'),
    path('auth/password_change/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='registration/password_change_done.html'),
         name='password_change_done'),
    path('auth/password_change/', CustomPasswordChangeView.as_view(success_url=reverse_lazy('accounts:password_change_done'),
                                                              template_name='registration/password_change.html'),
         name='password_change'),
    path('auth/password_reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_done.html'),
         name='password_reset_done'),
    path('auth/reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(success_url=reverse_lazy('accounts:password_change_done')),
         name='password_reset_confirm'),
    path('auth/password_reset/',
         auth_views.PasswordResetView.as_view(success_url=reverse_lazy('accounts:password_reset_done')),
         name='password_reset'),
]
