from datetime import timedelta
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from news.models import Post, Category
from django.conf import settings


def compose_obj(post):
    _post = {}
    _post['id'] = post.id
    _post['title'] = post.title
    return _post


def send_notification(subscriber, cat_obj):
    subject = f'Еженедельная рассылка новых публикаций'

    posts_info = {"category": '', "posts": []}

    for category, posts in cat_obj.items():
        posts_info["category"] = category
        posts_info["posts"] = [compose_obj(post) for post in posts]

    html = render_to_string(
        'mailing/weekly_notification.html',
        {
            'user_name': subscriber,
            'posts_info': posts_info,
        },
    )

    msg = EmailMultiAlternatives(
        subject=subject,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[subscriber.email, ],
    )
    msg.attach_alternative(html, "text/html")
    msg.send()


def weelky_news_job():
    for category in Category.objects.all():
        mailing_dict = {}  # инициализация переменной, пустой словарь <class 'dict'>
        cat_name = category.name
        postsForWeek = Post.objects.filter(
            postCategory=category, dateCreation__gte=timezone.now() - timedelta(weeks=1))
        if not postsForWeek:
            continue
            # вычисляем юзеров-подписчиков
        for subscriber in category.subscribers.all():  # берем каждого подписанта
            if subscriber not in mailing_dict:  # если объект юзер еще не содержится в словаре
                # добавляем объект юзера в качестве ключа, присваиваем value - пустой
                mailing_dict[subscriber] = {}
                # словарь
            # если категории еще нет
            if cat_name not in mailing_dict[subscriber]:
                mailing_dict[subscriber][cat_name] = set()  #
            # обращаемся к ключу вложенного словаря и
            mailing_dict[subscriber][cat_name].update(postsForWeek)
            # добавляем в него значение - все посты
            # категории за неделю

        for subscriber, cat_name in mailing_dict.items():
            send_notification(subscriber, cat_name)
