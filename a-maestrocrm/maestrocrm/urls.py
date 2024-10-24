from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

from core.views import index, about
from userprofile.forms import LoginForm, SignupForm

urlpatterns = [
    path('log-in/', auth_views.LoginView.as_view(template_name='userprofile/login.html', authentication_form=LoginForm), name='login'),
    # path('lead/', include('lead.urls')),
    path('about/', about, name='about'),
    path('dashboard/client/', include('client.urls')),
    path('dashboard/lead/', include('lead.urls')),
    path('dashboard/', include('userprofile.urls')),
    path('dashboard/team/', include('team.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('', index, name='index'),
    path('admin/', admin.site.urls),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)