from django.core.management.base import BaseCommand, CommandError
from eh_app.models import Student, Semester
import csv


class Command(BaseCommand):

    def handle(self, *app_labels, **options):
        with open('test.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)

            student = Student() #replace by object of desired input

            i = 0
            for row in reader:
                if i==0: #skip the header row
                    i += 1
                    continue

                cell_val = row[0] #UIN
                student.uin = cell_val
                print(cell_val)
                cell_val = row[2] #Last Name
                student.last_name = cell_val
                print(cell_val)
                cell_val = row[3] #First Name
                student.first_name = cell_val
                print(cell_val)
                cell_val = row[4] #Middle Name
                student.middle_name = cell_val
                print(cell_val)
                cell_val = row[7] #Email
                student.email = cell_val
                print(cell_val)
                cell_val = row[29] #start_semester
                student.first_tamu_semester = Semester.objects.filter(id=201811)[0] #replace 201811 with actual cell_val (need an existing Semester object)
                print(cell_val)
                cell_val = row[29] #graduation_semester
                student.graduation_semester = Semester.objects.filter(id=202211)[0] #replace 202211 with actual cell_val (need an existing Semester object)
                print(cell_val)

                student.save()
                i += 1
