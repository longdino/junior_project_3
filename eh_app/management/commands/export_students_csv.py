from django.core.management.base import BaseCommand, CommandError
from eh_app.models import Student
import csv


class Command(BaseCommand):

    def handle(self, *app_labels, **options):
        with open('test.csv', 'w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Last Name', 'First Name', 'Middle Name', 'UIN',
            'email', 'Major', 'GPA', 'Status Based on GPA Alone',
            'Status Based on Participation', 'Status GPA and Participation combined'])
            # writer.writerow(['Second row', 'A', 'B', 'C', '"Testing"', "Here's a quote"])

            # fields = Student._meta.get_fields()
            for student in Student.objects.all():
                row = []
                row.append(student.last_name)
                # print(student.last_name)
                row.append(student.first_name)
                row.append(student.middle_name)
                row.append(student.uin)
                row.append(student.email)
                row.append("major tbd")
                row.append(student.cumulative_gpa())
                row.append(student.status_gpa_alone())
                row.append(student.status_part_alone())
                row.append(student.status_gpa_and_part())
                writer.writerow(row)

            # for obj in Student.objects.all():
            #     row = ""
            #     print(obj)
            #     for field in fields:
            #         print(field)
            #         row += field + ","
            #     writer.writerow(row)
