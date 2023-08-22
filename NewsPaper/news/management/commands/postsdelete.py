from django.core.management.base import BaseCommand
from news.models import Post, Category


class Command(BaseCommand):
    # показывает подсказку при вводе "python manage.py <ваша команда> --help"
    help = 'Удаление новостей одной категории postsdelete <category_name>'

    def add_arguments(self, parser):
        parser.add_argument('category', type=str)

    def handle(self, *args, **options):
        answer = input(
            f'Вы правда хотите удалить все статьи в категории {options["category"]}? yes/no: \n')

        if answer == 'yes':
            try:
                category = Category.objects.get(name=options['category'])
                Post.objects.filter(postCategory=category).delete()
                self.stdout.write(self.style.SUCCESS(
                    f'Succesfully deleted all news from category {category.name}'))  # в случае неправильного подтверждения говорим, что в доступе отказано
            except:
                self.stdout.write(self.style.ERROR(
                    f'Could not find category "{options["category"]}"'))
        else:
            self.stdout.write(self.style.ERROR('Отменено'))
