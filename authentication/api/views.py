from rest_framework import permissions
from rest_framework_mongoengine import generics as mongo_generics

from authentication.models import Account
from authentication.api.serializers import AccountSerializer


class CreateAccountView(mongo_generics.CreateAPIView):

    model = Account
    permission_classes = [
        permissions.AllowAny]
    serializer_class = AccountSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            Account.create_user(**serializer.validated_data)


class AccountList(mongo_generics.ListCreateAPIView):
    model = Account
    queryset = Account.objects()
    serializer_class = AccountSerializer
    permission_classes = [permissions.AllowAny]


class AccountDetail(mongo_generics.RetrieveUpdateDestroyAPIView):
    model = Account
    queryset = Account.objects()
    serializer_class = AccountSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'username'