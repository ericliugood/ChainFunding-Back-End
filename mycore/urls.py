"""mycore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from allauth.account.views import confirm_email
from django.conf.urls import url

# mysearcher
from mysearcher.views import SearcherViewSet
from mywallet.views import WalletAddressViewSet,TransferLogsViewSet
from mynotice.views import NoticeViewSet


router = DefaultRouter()

router.register('search', SearcherViewSet)
router.register('wallet',WalletAddressViewSet)
router.register('transferlog',TransferLogsViewSet)
router.register('notice',NoticeViewSet)


urlpatterns = [
    path('myapi/', include(router.urls)),
    path('admin/', admin.site.urls),
    url(r'^rest-auth/', include('rest_auth.urls')),  # rest auth url
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),  # register url
    url(r'^account/', include('allauth.urls')),
    url(r'^accounts-rest/registration/account-confirm-email/(?P<key>.+)/$', confirm_email, name='account_confirm_email'),
]
