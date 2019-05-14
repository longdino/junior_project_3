from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
	def handle(self, *app_labels, **options):

		Group.objects.get_or_create(name='Advisor')
		Group.objects.get_or_create(name='Faculty')