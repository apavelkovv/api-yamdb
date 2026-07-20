from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.pagination import PageNumberPagination

from reviews.models import Category, Genre, Title

from users.permissions import (
    IsAdminOrReadOnly, 
    IsAdmin, 
    IsOwnerOrModeratorOrAdmin
)
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleReadSerializer,
    TitleWriteSerializer,
)


class CategoryViewSet(viewsets.ModelViewSet):
    """ViewSet для категорий."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(viewsets.ModelViewSet):
    """ViewSet для жанров."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    """ViewSet для произведений."""
    queryset = Title.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category__slug', 'genre__slug', 'name', 'year')
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return TitleWriteSerializer
        return TitleReadSerializer