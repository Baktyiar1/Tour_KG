from django.db.models import Count, Q, Sum, F
from rest_framework import generics, serializers, status
from rest_framework.exceptions import PermissionDenied
from django.core.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView, Response
from django.db import models
from .service import get_client_ip
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from .models import Tour, Region, Banner, TourAuthorRequest


from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters import rest_framework as filters

from .serializers import RegionIndexSerializer, BannerIndexSerializer, TourListSerializer, CreateRetingSerializer, \
    CreateTourSerializer, TourAuthorRequestSerializer, AuthorUserProfilSerializer, TourAuthorRequestStatusSerializer, \
    AuthorRequestListSerializer, AuthorRequestStatusListSerializer
from .pagination import RegionPagination
from .filters import TourFilter
from .permissions import IsAdminOrManager, IsAdminOrAuthor

User = get_user_model()
class BannerIndexView(generics.ListAPIView):
    queryset = Banner.objects.all()
    serializer_class = BannerIndexSerializer

class RegionIndexView(generics.ListAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionIndexSerializer

class RegionListView(generics.ListAPIView):
    serializer_class = TourListSerializer

    def get_queryset(self):
        region_id = self.kwargs.get('pk')
        client_ip = get_client_ip(self.request)

        return Tour.objects.filter(
            is_active=True,
            regions__id=region_id
        ).annotate(
            rating_user=Count('ratings', filter=Q(ratings__ip=client_ip))
        ).annotate(
            middle_star=Sum(F('ratings__star')) / Count('ratings')
        ).order_by('-middle_star')

class TourIndexView(generics.ListAPIView):
    serializer_class = TourListSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = TourFilter
    pagination_class = RegionPagination
    def get_queryset(self):
        client_ip = get_client_ip(self.request)

        return Tour.objects.filter(
            is_active=True,
        ).annotate(
            rating_user=Count('ratings', filter=Q(ratings__ip=client_ip))
        ).annotate(
            middle_star=Sum(F('ratings__star')) / Count('ratings')
        ).order_by('-middle_star')


class CreateTourView(generics.CreateAPIView):
    queryset = Tour.objects.all()
    serializer_class = CreateTourSerializer
    permission_classes = [IsAdminOrAuthor]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)












 # на разработке
class TourAuthorRequestCreateView(generics.CreateAPIView):
    queryset = TourAuthorRequest.objects.all()
    serializer_class = TourAuthorRequestSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Проверяем, подал ли пользователь уже заявку
        if TourAuthorRequest.objects.filter(user=self.request.user).exists():
            raise ValidationError('Вы уже подали заявку на роль автора.')
        # Сохраняем заявку и связываем её с пользователем
        serializer.save(user=self.request.user)

class AuthorTourRequesListView(generics.ListAPIView):
    serializer_class = AuthorRequestListSerializer
    permission_classes = [IsAdminOrManager]

    def get_queryset(self):
        return TourAuthorRequest.objects.filter(is_approved=False)



class TourAuthorRequestStatusView(generics.UpdateAPIView):
    queryset = TourAuthorRequest.objects.all()
    serializer_class = TourAuthorRequestSerializer
    permission_classes = [IsAdminOrManager]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.approve_author()
        return super().update(request, *args, **kwargs)

class AuthorRequestStatusListView(generics.ListAPIView):
    serializer_class = AuthorRequestStatusListSerializer
    permission_classes = [IsAdminOrManager]

    def get_queryset(self):
        return TourAuthorRequest.objects.filter(is_approved=True)


 # на разработке
class AuthorUserProfilViews(APIView):
    # permission_classes = [permissions.IsAuthenticated]

    # @swagger_auto_schema(responses={200: AuthorUserProfilSerializer()})
    def get(self, request):
        user = get_object_or_404(User, id=request.user.id)
        if user.is_author:  # Проверяем, является ли пользователь автором
            serializer = AuthorUserProfilSerializer(user)

        return Response(serializer.data)


















class AddStarRatingView(generics.CreateAPIView):
    serializer_class = CreateRetingSerializer

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))

