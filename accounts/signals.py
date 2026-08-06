import threading
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from .tasks import send_update_to_clients_task

@receiver(post_save, sender=User)
def send_to_clients(sender, instance, **kwargs):
    # Запускаем отправку в отдельном потоке, чтобы не блокировать ответ
    thread = threading.Thread(target=send_update_to_clients_task, args=(instance.id,))
    thread.daemon = True  # поток завершится вместе с основным процессом
    thread.start()