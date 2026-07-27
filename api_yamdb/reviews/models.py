from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


class Category(models.Model):
    """Модель категории (например, 'Книги', 'Фильмы', 'Музыка')."""
    name = models.CharField(
        max_length=256,
        verbose_name='Название категории'
    )
    slug = models.SlugField(max_length=50,
                            unique=True,
                            verbose_name='Уникальный слаг'
                            )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель жанра (например, 'Сказка', 'Рок', 'Артхаус')."""
    name = models.CharField(max_length=256, verbose_name='Название жанра')
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Уникальный слаг'
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель произведения."""
    name = models.CharField(
        max_length=256,
        verbose_name='Название произведения'
    )
    year = models.PositiveSmallIntegerField(
        verbose_name='Год выпуска',
        null=True,
        blank=True
    )
    description = models.TextField(
        verbose_name='Описание',
        null=True,
        blank=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='titles',
        verbose_name='Категория'
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанры'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('-year', 'name')

    def __str__(self):
        return self.name


class Review(models.Model):
    """Модель отзыва на произведениею."""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Заголовок отзыва'
    )
    text = models.TextField(verbose_name='Текст отзыва')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор отзыва'
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка',
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )
    pub_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name='Дата публикации')

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-pub_date',)
        constraints = [
            models.UniqueConstraint(
                fields=('author', 'title'),
                name='unique_review_per_title'
            )
        ]

    def __str__(self):
        return (f'Отзыв {self.id} на произведение'
                f'{self.title.name} от {self.author.username}')


class Comment(models.Model):
    """Модель комментария к отзыву."""
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )
    text = models.TextField(verbose_name='Текст комментария')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария'
    )
    pub_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name='Дата публикации')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date',)

    def __str__(self):
        return (f'Комментарий {self.id} к отзыву '
                f'{self.review.id} от {self.author.username}')
