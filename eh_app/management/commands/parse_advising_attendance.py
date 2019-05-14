from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
import csv, glob
from eh_app.models import Advisor, Semester, Student, StudentAdvisorMeeting

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('directory', nargs=1, type=str)

    def handle(self, *args, **options): # pragma: no cover
        path = options['directory'][0]

        set_coh = set()
        # Single column file containing UIN values
        with open(f'{path}/cohort.csv', 'r') as cohort_csv:
            cohort_data = [row for row in csv.reader(cohort_csv.read().splitlines())]
            for row in range(1,len(cohort_data)):
                set_coh.add(cohort_data[row][0])

        skip_count = 0
        row_holder = []
        for filename in glob.glob(f'{path}/*ADVISING_ATTENDANCE*.csv'):
            with open(filename, 'r') as f:
                advising_data = [row for row in csv.reader(f.read().splitlines())]
            for row in advising_data[1:]:
                if row[0] in set_coh:
                    row_holder.append(self.row_dict(row))
                else:
                    skip_count += 1

        fail_count = 0
        advisor_creation_count = 0
        advising_attendance_logged = 0
        for row in row_holder:
            (semester, _) = Semester.objects.get_or_create(id=row['sem_id'])
            try:
                student = Student.objects.get(uin=row['student_uin'])
            except Student.DoesNotExist:
                print(f'Error: Advising {row["date"]}-{row["details"]} could not be saved as student {row["student_uin"]} could not be found.')
                fail_count += 1
                continue

            # TODO: Add track in csv and parse or compare here
            (advisor, created) = Advisor.objects.get_or_create(uin=row['instructor_uin'])
            if created:
                advisor.first_name = row['instructor_first_name']
                advisor.middle_name = row['instructor_middle_name']
                advisor.last_name = row['instructor_last_name']
                advisor.save()
                advisor_creation_count += 1

            try:
                new_meeting = StudentAdvisorMeeting()
                new_meeting.date = row['date']
                new_meeting.details = row['details']
                new_meeting.student = student
                new_meeting.advisor = advisor
                new_meeting.semester = semester
                new_meeting.save()
                advising_attendance_logged += 1
            except IntegrityError: # pragma: no cover
                print(f'Skip: Advising tracking for student {row["student_uin"]} for meeting {row["date"]} - \"{row["details"]}\" could not be saved as it failed to be unique (non-duplicated).')
                skip_count += 1

        print(f"""
Advisors created: {advisor_creation_count}
Meeting attendances logged: {advising_attendance_logged}
Total Skipped: {skip_count} Failed: {fail_count}
        """);

    def row_dict(self, row):
        dict_temp = {}
        dict_temp['student_uin'] = (int)(row[0])
        dict_temp['sem_id'] = (int)(row[1])
        dict_temp['date'] = row[2]
        dict_temp['details'] = row[3]
        dict_temp['instructor_last_name'] = row[4]
        dict_temp['instructor_first_name'] = row[5]
        dict_temp['instructor_middle_name'] = row[6]
        dict_temp['instructor_uin'] = (int)(row[7])
        return dict_temp
