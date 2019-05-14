from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
import csv, glob, os, shutil
from eh_app.models import Campus, Course, Department, Section, Semester, Student, StudentSectionEnrollment, Teacher

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('directory', nargs=1, type=str)

    # Detailed testing coverage provided by sensitive data
    def handle(self, *args, **options): # pragma: no cover
        path = options['directory'][0]

        set_coh = set()
        # Single column file containing UIN values
        with open(f'{path}/cohort.csv', 'r') as cohort_csv:
            cohort_data = [row for row in csv.reader(cohort_csv.read().splitlines())]
            for row in range(1,len(cohort_data)):
                set_coh.add(cohort_data[row][0])

        skip_count = 0
        list_row_holder = []
        for filename in glob.glob(f'{path}/*COURSES_TAKEN*.csv'):
            with open(filename, 'r') as f:
                data = [row for row in csv.reader(f.read().splitlines())]
            # NOTE: The following tracks classes provided they're either honors or not tbd
            # NOTE: Standardization of column naming could allow csv.dictreader usage (reduction of the following assignments)
            for row in data[1:]:
                # First column is student UIN
                if row[0] in set_coh:
                    # Check to see if course number is given (if not, expected value is 'XXX')
                    if row[12] != 'XXX':   # Allowing 'XXX' can violate data integrity
                        # # FIXME: Why is this exclusion necessary?
                        # if((int)(data[x][12]) >= 600 or data[x][12].endswith('91') or data[x][12].endswith('85')):
                        (row_dict, skipped) = self.row_dict(row)
                        if not skipped:
                            list_row_holder.append(row_dict)
                        else:
                            skip_count += 1
                    else:
                        skip_count += 1
                else:
                    skip_count += 1

        course_creation_count = 0
        section_creation_count = 0
        teacher_creation_count = 0
        enrollment_creation_count = 0
        fail_count = 0
        for row in list_row_holder:
            # Course creation: (number, title, credits, min_credits(optional), max_credits(optional), relations: (track?))
            (department, _) = Department.objects.get_or_create(name=row['department'])

            # Check if something with unique defining values exists, returns (object, created)
            try:
                course = Course.objects.get(
                    number=row['course'],
                    department=department
                )
            except Course.DoesNotExist:
                # Teacher creation: (uin, first_name, last_name, middle_name)
                course = Course()
                course.number = row['course']
                course.department = department
                course.title = row['title']
                course.credits = row['hours']
                course.min_credits = row['hours']
                course.save()
                course_creation_count += 1

            (teacher, created) = Teacher.objects.get_or_create(uin=row['instructor_uin'])
            if created:
                teacher.first_name = row['instructor_first_name']
                teacher.middle_name = row['instructor_middle_name']
                teacher.last_name = row['instructor_last_name']
                teacher.save()
                teacher_creation_count += 1

            # Section creation: (crn, number, level, relations: (course, teacher, semester, campus))
            # Relations
            (semester, _) = Semester.objects.get_or_create(id=row['sem_id'])
            (campus, _) = Campus.objects.get_or_create(name=row['campus'])

            # Check if something with unique defining values exists, returns (object, created)
            try:
                section = Section.objects.get(
                    crn=row['crn'],
                    semester=semester,
                    campus=campus
                )
            except Section.DoesNotExist:
                section = Section()
                section.crn = row['crn']
                section.semester = semester
                section.course = course
                # FIXME: Need formatting that can be split for co-teaching, current is not possible to reliably split
                section.campus = campus
                section.number = row['section']
                section.level = row['level']
                section.eh = row['honors']
                section.save()
                section.teachers.add(teacher)
                section_creation_count += 1 # This will be triggered on a second run but does not create duplicates

            # Student_section_enrollment creation: (grade, grading_mode, repeat, relations:(student, section))
            try:
                student = Student.objects.get(uin=row['student_uin'])
            except Student.DoesNotExist:
                print(f'Error: Course {row["department"]}-{row["course"]}-{row["section"]} could not be saved as student {row["student_uin"]} could not be found.')
                fail_count += 1
                continue

            try:
                new_enrollment = StudentSectionEnrollment()
                new_enrollment.grade = row['grade']
                new_enrollment.grading_mode = row['grading_mode']
                new_enrollment.repeat = row['repeat']
                new_enrollment.student = student
                new_enrollment.section = section
                new_enrollment.save()
                enrollment_creation_count += 1
            except IntegrityError:
                print(f'Skip: Enrollment for student {row["student_uin"]} on section {row["department"]}-{row["course"]}-{row["section"]} could not be saved as it failed to be unique (non-duplicated).')
                skip_count += 1

        print(f"""
Courses created: {course_creation_count}
Sections created: {section_creation_count}
Teachers created: {teacher_creation_count}
Enrollments created: {enrollment_creation_count}
Total Skipped: {skip_count} Failed: {fail_count}
        """);

    # Detailed testing coverage provided by sensitive data
    def row_dict(self, row) -> (dict, bool): # pragma: no cover
        dict_temp = {}
        dict_temp['student_uin'] = (int)(row[0])
        dict_temp['department'] = row[4]
        dict_temp['sem_id'] = (int)(row[6])
        dict_temp['campus'] = row[8]
        dict_temp['level'] = row[9]
        dict_temp['crn'] = row[10]
        dict_temp['subject'] = row[11]
        dict_temp['course'] = (int)(row[12])
        try:    # NOTE: Some sections have non int fields (e.g., 'M30'), this is a data integrity issue
            dict_temp['section'] = (int)(row[13])
        except:
            print(f'Skip: Course {dict_temp["department"]}-{dict_temp["course"]}-{row[13]} section is not an int type.')
            return (None, True)
        if row[14] != '':
            dict_temp['hours'] = (int)(row[14])
        else:
            print(f'Skip: Course {dict_temp["department"]}-{dict_temp["course"]}-{dict_temp["section"]} hours not provided.')
            return (None, True)
        if row[15] != '':
            dict_temp['grade'] = row[15] # Includes S/U
        else:
            print(f'Skip: Course {dict_temp["department"]}-{dict_temp["course"]}-{dict_temp["section"]} grade not provided.')
            return (None, True)
        dict_temp['grading_mode'] = (row[16]) # G/S, L/N/T/X and others
        dict_temp['repeat'] = row[17]
        dict_temp['title'] = (row[18])  # A/I, not sure about the meaning of these values
        if row[26] != '':
            dict_temp['instructor_last_name'] = row[21]
            dict_temp['instructor_first_name'] = row[22]
            dict_temp['instructor_middle_name'] = row[23]
            dict_temp['instructor_uin'] = (int)(row[26])
        else:
            dict_temp['instructor_last_name'] = 'TBD'
            dict_temp['instructor_first_name'] = 'TBD'
            dict_temp['instructor_middle_name'] = 'TBD'
            dict_temp['instructor_uin'] = 0
        dict_temp['honors'] = self.row_is_honors(row)
        return (dict_temp, False)

    def row_is_honors(self, row):
        return (('HNR' in row[18]) or ('HONOR' in row[18]) or ('HONORS' in
            row[18]) or ('HONR' in row[18]))
