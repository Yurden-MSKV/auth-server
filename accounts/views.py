from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login
from oauth2_provider.decorators import protected_resource

from .forms import CustomUserCreationForm, UserEditForm
from .models import User


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            pass
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@protected_resource()
def user_info(request):
    user = request.resource_owner
    if not user:
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    return JsonResponse({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'is_superuser': user.is_superuser,
        'pic': request.build_absolute_uri(user.pic.url) if user.pic else None
    })


from oauth2_provider.views import AuthorizationView as BaseAuthorizationView
from oauth2_provider.models import get_application_model
from django.shortcuts import redirect

Application = get_application_model()


class AutoAuthorizationView(BaseAuthorizationView):
    """Автоматически одобряет запросы от доверенных приложений."""

    def get(self, request, *args, **kwargs):
        # Получаем приложение по client_id
        client_id = request.GET.get('client_id')
        if client_id:
            try:
                application = Application.objects.get(client_id=client_id)
                # Если приложение помечено как skip_authorization
                if application.skip_authorization:
                    # Эмулируем POST-запрос с разрешением
                    request.method = 'POST'
                    request.POST = request.POST.copy()
                    request.POST['allow'] = 'Authorize'
            except Application.DoesNotExist:
                pass

        return super().get(request, *args, **kwargs)

def index(request):
    if request.user.is_authenticated:
        return redirect('profile_page')
    else:
        return redirect('login')

def profile_page(request):
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        return render(request, 'profile_page.html', {'user': user})
    else:
        return HttpResponse('Ты не залогинен.')

@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = UserEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile_page')
    else:
        form = UserEditForm(instance=request.user)

    return render(request, 'profile_edit.html', {'form': form})