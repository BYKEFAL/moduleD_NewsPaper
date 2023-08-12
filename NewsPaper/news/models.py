from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.SmallIntegerField(default=0)

    def update_rating(self):     # Рейтинг состоит из следующих слагаемых:
        #  суммарный рейтинг статей автора умножается на 3;
        postRat = self.post_set.all().aggregate(sum=Sum('rating'))['sum'] * 3
        #  суммарный рейтинг все.х комментариев автора;
        userRat = self.authorUser.comment_set.all(
        ).aggregate(sum=Sum('rating'))['sum']
        #  суммарный рейтинг всех комментариев к статьям автора.
        commentRat = Comment.objects.filter(
            commentPost__author=self).aggregate(sum=Sum('rating'))['sum']
        self.ratingAuthor = postRat + userRat + commentRat
        self.save()

    def __str__(self) -> str:
        return self.authorUser.username


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)
    subscribers = models.ManyToManyField(User, blank=True)

    def get_category(self):
        return self.name

    def __str__(self) -> str:
        return self.name


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOICES = (
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья'),
    )
    categoryType = models.CharField(
        max_length=2, choices=CATEGORY_CHOICES, default=ARTICLE)
    dateCreation = models.DateTimeField(auto_now_add=True)
    postCategory = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=128)
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[:124] + '...'

    def __str__(self) -> str:
        return f'{self.title} {self.preview()}'

    # добавим абсолютный путь, чтобы после создания нас перебрасывало на страницу с постом
    def get_absolute_url(self):
        return f'/news/{self.id}'


class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return self.commentUser.username
