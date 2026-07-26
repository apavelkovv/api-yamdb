from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий."""
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для жанров."""
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class CategoryMinifiedSerializer(serializers.ModelSerializer):
    """Сериализатор категории для вложенного отображения в Title."""
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreMinifiedSerializer(serializers.ModelSerializer):
    """Сериализатор жанра для вложенного отображения в Title."""
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализатор для произведений (GET-запросы)."""
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.IntegerField(read_only=True, default=None)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating',
            'description', 'genre', 'category'
        )


class TitleWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для произведений (POST, PUT, PATCH)."""
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для отзывов."""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('id', 'pub_date')

    def validate(self, data):
        request = self.context['request']
        if request.method == 'POST':
            title_id = self.context['view'].kwargs.get('title_id')
            if Review.objects.filter(
                title=title_id,
                author=request.user
            ).exists():
                raise serializers.ValidationError(
                    'Вы уже оставили отзыв на это произведение'
                )
        return data

    def validate_score(self, value):
        """Валидация поля score."""
        if not 1 <= value <= 10:
            raise serializers.ValidationError(
                'Оценка должна быть от 1 до 10'
            )
        return value


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для комментариев."""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('id', 'pub_date')
