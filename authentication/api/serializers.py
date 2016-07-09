from django.contrib.auth import update_session_auth_hash
from authentication.models import Account
from rest_framework_mongoengine.serializers import (
    DocumentSerializer, drf_fields)


class AccountSerializer(DocumentSerializer):
    password = drf_fields.CharField(write_only=True, required=False)
    confirm_password = drf_fields.CharField(write_only=True, required=False)

    class Meta:
        model = Account
        fields = ('id', 'email', 'username', 'date_joined', 'is_superuser',
                  'first_name', 'last_name', 'password', 'confirm_password',)
        read_only_fields = ('date_joined',)

        def create(self, validated_data):
            return Account.create(**validated_data)

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