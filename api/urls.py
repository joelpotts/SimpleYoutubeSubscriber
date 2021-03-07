from django.urls import include, path

from rest_framework.authtoken.views import obtain_auth_token
from rest_framework import routers

from api import views


router = routers.DefaultRouter()
router.register(r'subscriptions', views.SubscriptionView)

urlpatterns = [
    path('register/', views.UserCreate.as_view(), name="register"),
    path('authenticate/', obtain_auth_token, name='authenticate'),
    path('videos/', views.ProcessedVideoDataView.as_view(), name="videos"),
    path('', include(router.urls)),
]