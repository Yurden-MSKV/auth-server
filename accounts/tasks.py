import requests
from celery import shared_task
from django.conf import settings

from accounts.models import User


@shared_task(bind=True, max_retries=3)
def send_update_to_clients_task(self, user_id):
    try:
        user = User.objects.prefetch_related('authenticated').get(id=user_id)
        user_auth_sites = list(user.authenticated.filter(is_active=True).values('link'))
        headers = {
            'Authorization': f'Bearer {settings.SYNC_SECRET}',
            'Content-Type': 'application/json',
                   }

    except User.DoesNotExist:
        return

    payload = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "is_staff": user.is_staff,
        'is_active': user.is_active,

        "pic": user.get_pic_url() if hasattr(user, 'get_pic_url') else None,
        "bio": getattr(user, 'bio', ''),
    }

    for client in user_auth_sites:
        try:
            response = requests.post(
                f"{client['link']}",
                json=payload,
                headers=headers,
                timeout=5,
                )
            response.raise_for_status()
        except Exception as e:
            self.retry(exc=e, countdown=60)