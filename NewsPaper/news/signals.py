from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Post, Category
from django.conf import settings


@receiver(m2m_changed, sender=Post.postCategory.through)
def new_post_notify_user(sender, instance, action, **kwargs):
    # Новая статья была создана
    if action == 'post_add':
        subscribers = instance.postCategory.values(
            'name', 'subscribers__email', 'subscribers__username')

        for i in subscribers:
            category = i.get('name')
            html = render_to_string(
                'mailing/news_post_notification.html',
                {
                    'post': instance,
                    'category': category,
                },
            )

            msg = EmailMultiAlternatives(
                subject=f'Здравствуй, {i.get("subscribers__username")}. Новая статья в твоём любимом разделе!',
                body='',
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[i.get("subscribers__email"),],
                # to=[settings.MY_TEST_EMAIL,],
            )

            msg.attach_alternative(html, 'text/html')
            try:
                msg.send()
            except Exception as e:
                print(e)
