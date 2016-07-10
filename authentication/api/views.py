import logging
logger = logging.getLogger(__name__)

from django.utils.encoding import smart_text
from django.contrib.auth import login
from mongoengine.django.auth import MongoEngineBackend, get_user, User

from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.authentication import authenticate
from rest_framework_mongoengine import generics as mongo_generics

from authentication.models import Account
from authentication.api.serializers import AccountSerializer, LoginSerializer


class RegisterAccountView(mongo_generics.CreateAPIView):

    model = Account
    permission_classes = [permissions.AllowAny]
    serializer_class = AccountSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            Account.create_user(**serializer.validated_data)


class LoginView(mongo_generics.GenericAPIView):

    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        account = authenticate(username=username, password=password)

        if account is not None:
            if account.is_active:
                user = get_user(account.id)

                # FIX to make mongoengine 0.9.0 works with Django 1.9.7
                User._meta.pk = User._fields["id"]
                User._meta.pk.value_to_string = lambda obj: smart_text(obj.pk)
                User.backend = account.backend

                login(request, user)

                return Response(LoginSerializer(account).data)

            else:
                return Response({
                    'status': 'Unauthorized',
                    'message': 'This account has been disabled.'
                }, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({
                'status': 'Unauthorized',
                'message': 'Username/password combination invalid.'
            }, status=status.HTTP_401_UNAUTHORIZED)


class AccountList(mongo_generics.ListCreateAPIView):
    model = Account
    queryset = Account.objects()
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated,]


class AccountDetail(mongo_generics.RetrieveUpdateDestroyAPIView):
    model = Account
    queryset = Account.objects()
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated,]
    lookup_field = 'username'
