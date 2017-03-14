"""www_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from rango import views
from django.conf.urls import include

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^rango/', include('rango.urls')),
    url(r'^accounts/register/$', views.MyRegistrationView.as_view(), name='registration_register'),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

## registration.backends.simple.urls mappings
# registration -> /accounts/register/
# registration complete -> /accounts/register/complete/
# login -> /accounts/login/
# logout -> /accounts/logout/
# password change -> /password/change/
# password reset -> /password/reset/
# activation complete (used in the two-step registration) -> activate/complete/
# activate (used if the account action fails) -> activate/<activation_key>/

# ^accounts/ ^register/closed/$ [name='registration_disallowed']
# ^accounts/ ^register/complete/$ [name='registration_complete']
# ^accounts/ ^register/$ [name='registration_register']
# ^accounts/ ^login/$ [name='auth_login']
# ^accounts/ ^logout/$ [name='auth_logout']
# ^accounts/ ^password/change/$ [name='auth_password_change']
# ^accounts/ ^password/change/done/$ [name='auth_password_change_done']
# ^accounts/ ^password/reset/$ [name='auth_password_reset']
# ^accounts/ ^password/reset/complete/$ [name='auth_password_reset_complete']
# ^accounts/ ^password/reset/done/$ [name='auth_password_reset_done']
# ^accounts/ ^password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$ [name='auth_password_reset_confirm']
