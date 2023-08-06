from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'profile/profile_index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(
            name='author_group').exists()
        return context

# Добавляем функциональное представление для повышения привилегий пользователя до членства в группе premium


@login_required
def upgrade_me(request):
    user = request.user
    author = Group.objects.get(name='author_group')
    if not request.user.groups.filter(name='author_group').exists():
        author.user_set.add(user)
    return redirect('/profile')
