from django.core.management.base import BaseCommand
import pandas as pd


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        self.stdout.write(f'Generating data from Excel file')


