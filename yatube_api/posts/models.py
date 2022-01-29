from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    title = models.CharField(
        'Название группы',
        max_length=200,
        help_text='Название новой группы'
    )
    slug = models.SlugField(
        'Адрес группы',
        unique=True,
        help_text='Адрес новой группы'
    )
    description = models.TextField(
        'Описание группы',
        help_text='Описание новой группы'
    )

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField(
        'Текст поста',
        help_text='Текст нового поста'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        help_text='Дата публикации нового поста'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор',
        help_text='Автор нового поста'
    )
    image = models.ImageField(
        'Картинка',
        upload_to='posts/',
        null=True,
        blank=True,
        help_text='Картинка поста'
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Группа',
        related_name='posts',
        help_text='Группа, к которой будет относиться пост'
    )

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор',
        help_text='Автор нового поста'
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name='Комментарий',
        related_name='comments',
        help_text='Комментарий к посту'
    )
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True,
        help_text='Дата комментария поста'
    )


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followed_user',
        verbose_name='Подписчик',
        help_text='Пользователь, который подписан'
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Автор для подписки',
        help_text='Пользователь, на которого подписываются'
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'following'),
                name='unique_follow'
            ),
        )

    def __str__(self):
        return f'{self.user} подписан на {self.following}'
