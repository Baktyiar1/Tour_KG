from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import Response, APIView
from rest_framework import generics, permissions
from rest_framework import status
from tour.permissions import IsAdminOrAuthor
from .models import MyUser
from .serializers import (
    CustomRegisterSerializer, UserProfilSerializer, UserProfilUpdateSerializer, UserBookingSerializer,
    AuthorUserProfilSerializer, QrCodeSerializer
)



class UserRegisterViews(generics.CreateAPIView):
    queryset = MyUser.objects.all()
    serializer_class = CustomRegisterSerializer

    def perform_create(self, serializer):
        # Передаем request в сериализатор
        serializer.save(request=self.request)


class UserProfilViews(APIView):
    permission_classes = [permissions.IsAuthenticated]
    @swagger_auto_schema(responses={200: UserProfilSerializer()})
    def get(self, request):
        user = get_object_or_404(MyUser, id=request.user.id)
        serializer = UserProfilSerializer(user)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=UserProfilUpdateSerializer,
        responses={200: UserProfilUpdateSerializer}
    )
    def patch(self, request):
        user = get_object_or_404(MyUser, id=request.user.id)
        serializer = UserProfilUpdateSerializer(user, data=request.data, partial=True)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)


# class UserLogoutView(APIView):
#
#     def post(self, request):
#         request.session.flush()
#         return Response(data='good', status=status.HTTP_200_OK)


class UserBookingView(generics.ListAPIView):
    serializer_class = UserBookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return MyUser.objects.filter(id=self.request.user.id)  # Возвращаем текущего пользователя


class AuthorToursView(generics.ListAPIView):
    serializer_class = AuthorUserProfilSerializer

    def get_queryset(self):
        return MyUser.objects.filter(id=self.request.user.id)

class QrCodeView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrAuthor]
    serializer_class = QrCodeSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_admin:
            return MyUser.objects.all()
        return MyUser.objects.filter(id=user.id)
