from django.core.management.base import BaseCommand
import csv, glob
from eh_app.models import Activity, Semester, Student

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('directory', nargs=1, type=str)

    def handle(self, *args, **options):  # pragma: no cover
        path = options['directory'][0]

        set_coh = set()
        # Single column file containing UIN values
        with open(f'{path}/cohort.csv', 'r') as cohort_csv:
            cohort_data = [row for row in csv.reader(cohort_csv.read().splitlines())]
            for row in range(1,len(cohort_data)):
                set_coh.add(cohort_data[row][0])

        skip_count = 0
        row_holder = []
        for filename in glob.glob(f'{path}/*ACTIVITY_ATTENDANCE*.csv'):
            with open(filename, 'r') as f:
                activity_data = [row for row in csv.reader(f.read().splitlines())]
            for row in activity_data[1:]:
                if row[0] in set_coh:
                    row_holder.append(self.row_dict(row))
                else:
                    skip_count += 1

        fail_count = 0
        activities_created = 0
        activity_attendance_logged = 0
        for row in row_holder:
            (semester, _) = Semester.objects.get_or_create(id=row['sem_id'])
            try:
                student = Student.objects.get(uin=row['student_uin'])
            except Student.DoesNotExist:
                print(f'Error: Activity {row["date"]}-{row["location"]} could not be saved as student {row["student_uin"]} could not be found.')
                fail_count += 1
                continue

            (activity, created) = Activity.objects.get_or_create(
                date=row['date'],
                location=row['location'],
                details=row['details'],
                semester=semester
            )
            if created:
                activities_created += 1

            (success, error_msg) = student.add_activity_attendance(activity)
            if success:
                activity_attendance_logged += 1
            else: # pragma: no cover
                print(error_msg)
                fail_count += 1

        print(f"""
Activities created: {activities_created}
Activity attendances logged: {activity_attendance_logged}
Total Skipped: {skip_count} Failed: {fail_count}
        """);

    def row_dict(self, row):
        dict_temp = {}
        dict_temp['student_uin'] = (int)(row[0])
        dict_temp['sem_id'] = (int)(row[1])
        dict_temp['date'] = row[2]
        dict_temp['location'] = row[3]
        dict_temp['details'] = row[4]
        return dict_temp
