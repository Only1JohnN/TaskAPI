from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from .models import CustomUser
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken

class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'password')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            raise ValidationError("Passwords do not match")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data["password"]
        user.set_password(password)
        if commit:
            user.save()
        return user

class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = '__all__'

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = ('first_name', 'last_name', 'email', 'phone_number', 'is_email_verified', 'is_phone_verified', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'is_email_verified', 'is_phone_verified')
    fieldsets = (
        (None, {'fields': ('email', 'phone_number', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'profile_picture')}),
        ('Permissions', {'fields': ('is_email_verified', 'is_phone_verified', 'is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone_number', 'first_name', 'last_name', 'password', 'confirm_password', 'is_email_verified', 'is_phone_verified', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    readonly_fields = ('date_joined', 'last_login')
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        obj.save()  # Explicitly save the object to ensure changes are applied


# Register CustomUser with CustomUserAdmin
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.unregister(BlacklistedToken)
admin.site.unregister(OutstandingToken)
