from rest_framework.views import APIView, Request, Response, status
from .models import Account
from .serializers import AccountSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404
from .permissions import IsAccountOwnerOrAdmin



class AccountView(APIView):
    def get(self, request: Request) -> Response:
        account = Account.objects.all()

        serializer = AccountSerializer(account, many=True)

        return Response(serializer.data, status.HTTP_200_OK)


    def post(self, request: Request) -> Response:
        serializer = AccountSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)


class AccountDetailView(APIView):
    authentication_classes = [JWTAuthentication]

    permission_classes = [IsAuthenticated, IsAccountOwnerOrAdmin]

    def get(self, request: Request, user_id: int):
        user = get_object_or_404(Account, pk=user_id)

        self.check_object_permissions(request=request, obj=user)

        serializer = AccountSerializer(user)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    

    def patch(self, request: Request, user_id: int):
        user = get_object_or_404(Account, pk=user_id)

        self.check_object_permissions(request=request, obj=user)

        serializer = AccountSerializer(user, data=request.data, partial=True)

        serializer.is_valid()
    
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

class LoginJWTView(TokenObtainPairView):
    ...