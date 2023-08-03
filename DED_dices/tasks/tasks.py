from django.core.management.base import BaseCommand
from DED_dices.models import *

class DeleteChat(BaseCommand):
    help = 'Deletar chat'

    def handle(self, *args, **options):
        # Coloque seu código personalizado aqui
        messages = Message.objects.all()
        messages.delete()

if __name__ == '__main__':
    DeleteChat().handle()