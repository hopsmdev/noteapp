import logging
logger = logging.getLogger(__name__)

from django.contrib.auth import login, logout, get_user, authenticate
from rest_framework import permissions, status
from rest_framework.response import Response
#from rest_framework.authentication import authenticate, get_user
from rest_framework_mongoengine import generics as mongo_generics

from authentication.models import Account
from authentication.api.serializers import AccountSerializer, LoginSerializer


class RegisterAccountView(mongo_generics.CreateAPIView):

    model = Account
    permission_classes = [permissions.AllowAny]
    serializer_class = AccountSerializer

    def create(self, request):

        serializer = self.serializer_class(data=request.data)

        try:
            if serializer.is_valid(raise_exception=True):
                user = Account.create_user(**serializer.validated_data)
                print("REGISTER: ", user)
                return Response(
                    serializer.validated_data, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    'status': 'Bad request',
                    'message': 'Account could not be created with received data.'
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as exc:
            print(exc, request.data['username'])
            return Response({
                'status': 'Bad request',
                'message': str(exc)
            }, status=status.HTTP_400_BAD_REQUEST)


class LoginView(mongo_generics.GenericAPIView):

    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        print(username, password)

        account = authenticate(
            username=username, password=password)

        if account is not None:
            if account.is_active:
                login(request, account)
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


class LogoutView(mongo_generics.GenericAPIView):

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):

        logout(request)
        return Response({}, status=status.HTTP_204_NO_CONTENT)


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
