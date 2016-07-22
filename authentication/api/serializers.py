import logging
logger = logging.getLogger(__name__)

from django.contrib.auth import update_session_auth_hash
from authentication.models import Account
from rest_framework_mongoengine.serializers import (
    DocumentSerializer, drf_fields)
from rest_framework.reverse import reverse
from rest_framework.serializers import SerializerMethodField


class LoginSerializer(DocumentSerializer):
    username = drf_fields.CharField(required=True)
    password = drf_fields.CharField(write_only=True)

    class Meta:
        model = Account
        fields = ('username', 'password')


class AccountSerializer(DocumentSerializer):

    links = SerializerMethodField()

    password = drf_fields.CharField(write_only=True, required=False)
    confirm_password = drf_fields.CharField(write_only=True, required=False)

    class Meta:
        model = Account
        fields = ('id', 'email', 'username', 'date_joined', 'first_name',
                  'last_name', 'password', 'confirm_password', 'links')
        read_only_fields = ('date_joined',)

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)

        instance.save()

        password = validated_data.get('password', None)
        confirm_password = validated_data.get('confirm_password', None)

        if password and confirm_password and password == confirm_password:
            instance.set_password(password)
            instance.save()

        update_session_auth_hash(self.context.get('request'), instance)

        return instance

    def get_links(self, obj):
        request = self.context['request']
        return {
            "self": reverse(
                'account-detail',
                kwargs={'username': obj.username},
                request=request)
        }