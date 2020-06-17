from django.contrib import admin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext, gettext_lazy as _

from .models import Profile, UserAccount, Education, Specialization, NameEducationalInstitution, TypeWork, WorkPrice, \
    Comment


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = UserAccount
        fields = ('username', 'email', 'profile')


@admin.register(UserAccount)
class UserAdmin(UserAdmin):
    list_display = ('username', 'email', 'get_full_name')
    search_fields = ('username', 'email', 'patronymic', 'name', 'surname')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'profile')}),
        # (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_form = CustomUserCreationForm
    add_fieldsets = (
        ("TEST", {
            'classes': ('wide',),
            'fields': ('username', 'email', 'profile', 'password1', 'password2'),
        }),
    )


@admin.register(Profile)
class OrgProfileAdmin(admin.ModelAdmin):
    list_display = ['surname', 'name', 'patronymic', 'avatar_tag', 'phone_number']
    readonly_fields = ['avatar_tag']
    search_fields = ['patronymic', 'name', 'surname', 'phone_number']


@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    search_fields = ['name']


@admin.register(WorkPrice)
class WorkPriceAdmin(admin.ModelAdmin):
    search_fields = ['name']


@admin.register(NameEducationalInstitution)
class NameEducationalInstitutionAdmin(admin.ModelAdmin):
    search_fields = ['name']


@admin.register(TypeWork)
class TypeWorkAdmin(admin.ModelAdmin):
    search_fields = ['name']


@admin.register(Education)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ['name_university',]
    search_fields = ['name_university',]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'user_comment', 'text_message']
    search_fields = ['user','user_comment']