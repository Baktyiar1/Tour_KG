from django.db.models import Count, Q, Sum, F
from rest_framework import generics, serializers, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView, Response
from django.db import models
from .service import get_client_ip
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from .models import Tour, Region, Banner, TourAuthorRequest



User = get_user_model()

from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters import rest_framework as filters

from .serializers import RegionIndexSerializer, BannerIndexSerializer, TourListSerializer, CreateRetingSerializer, \
    CreateTourSerializer, TourAuthorRequestSerializer, AuthorUserProfilSerializer
from .pagination import TourPagination

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
    filter_backends = (filters.DjangoFilterBackend, SearchFilter)
    search_fields = ('title', 'description')
    pagination_class = TourPagination
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

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)







 # на разработке
class TourAuthorRequestCreateView(generics.CreateAPIView):
    queryset = TourAuthorRequest.objects.all()
    serializer_class = TourAuthorRequestSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        if user.status == 4:
            raise serializers.ValidationError("Вы уже являетесь автором.")

        author_request = serializer.save(user=user)
        author_request.approve_author()
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

