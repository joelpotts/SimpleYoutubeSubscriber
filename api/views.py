from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User


from rest_framework import generics
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from api.models import Subscription
from api.serializers import UserSerializer, SubscriptionSerializer
from api import utils


class SubscriptionView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)

    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Sets the user profile to the logged in User."""
        serializer.save(user=self.request.user)


class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny, )


class ProcessedVideoDataView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        processed_videos = utils.get_subscription_videos(request.user)
        content = {'results': processed_videos}
        return JsonResponse(content)