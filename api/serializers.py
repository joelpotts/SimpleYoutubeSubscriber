from rest_framework import serializers

from django.contrib.auth.models import User

from api import utils
from api.models import Subscription

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        exclude = ("user",)

    def validate_channel(self, value):
        if not utils.request_channel_page(value):
            raise serializers.ValidationError('The submitted channel id is not valid.')
        return value