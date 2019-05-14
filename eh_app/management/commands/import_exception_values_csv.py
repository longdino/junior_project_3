from django.core.management.base import BaseCommand, CommandError
from django.apps import apps
from django.db.utils import IntegrityError
import csv
from eh_app.models import Exception as ModelException, ActivityAdvisingException, Department

class Command(BaseCommand):

    def handle(self, *args, **options):
        count = 0
        skipped = 0
        # Using list call since files are smaller and need to be read from multiple times
        activity_data = list(csv.DictReader(open('eh_app/fixtures/ActivityException.csv'), delimiter=','))
        advising_data = list(csv.DictReader(open('eh_app/fixtures/AdvisingException.csv'), delimiter=','))
        fieldnames_ac = [key for key in activity_data[0]]
        fieldnames_ad = [key for key in advising_data[0]]
        # Checking if dimensions, and names match
        if fieldnames_ac != fieldnames_ad:
            return 'Field names do not match in the exception files.'
        if [row['Exception'] for row in activity_data] != [row['Exception'] for row in advising_data]:
            return 'Given exception fields do not match. (Possibly ordering or spelling).'

        for (row_ac, row_ad) in zip(activity_data, advising_data):
            try:
                exception = ModelException.objects.get(name=row_ac[fieldnames_ac[0]])    # [('Exception', 'Withdrew'), ...] Tuple of elements with column name first
            except ModelException.DoesNotExist:
                return """Exception {} does not exist.
                It may be spelled differently than in the Exception.yaml fixture.""".format(fieldnames_ac[0])

            # Fieldnames is the first row on the csv (department names)
            for dept in fieldnames_ac[1:]:    # Skipping past first column
                exception_relation = ActivityAdvisingException()
                exception_relation.exception = exception
                exception_relation.department = Department.objects.get(name=dept)
                exception_relation.activities_per_sem = row_ac[dept]
                exception_relation.advising_per_sem = row_ad[dept]

                try:
                    exception_relation.save()
                    count += 1
                except IntegrityError:
                    skipped += 1
                except Exception as e:
                    return '{}\nError in saving model {}'.format(e, exception_relation)

        return 'Total of {} inserted and {} skipped'.format(count, skipped)
