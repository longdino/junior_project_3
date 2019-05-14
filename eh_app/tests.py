import os
from django.test import TestCase
from eh_app.models import EmailTemplate, GPAStatus, Semester, Student, StudentSectionEnrollment, StudentSemesterStatus
from django.urls import reverse
from .forms import advisor_filter_form,ADVISOR_CATEGORY_FILTER_OPTIONS,faculty_filter_form,FACULTY_CATEGORY_FILTER_OPTIONS,superuser_filter_form,SEMESTER_STATUS_CATEGORIES,SUPERUSER_CATEGORY_FILTER_OPTIONS,STUDENT_FILTER_OPTIONS
from django.contrib.auth.models import User
from django.contrib.auth.models import Group, Permission
from django.core.management import call_command
from eh_app.views import studentList


TEST_SEED_FIXTURES = [
    'Department',
    'EmailTemplate',
    'GPADefAndStatus',
    'GPAandPartDef',
    'ProbDefStatus',
    'ParticipationStatus',
    'Requirement',
    'Tracks',
    'test_seed',
]
class TestViews(TestCase):
	def test_login_form(self):
		self.client.login(username='admin', password='admin')
		response = self.client.get('')
		self.assertTemplateUsed(response, 'eh_app/index.html')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.context['form'], superuser_filter_form().as_ul())
		self.assertContains(response,"utf-8")

	def test_login_superuser_form(self):
		user = User.objects.create_superuser('admin', 'gg@tt.com', 'admin')
		self.client.login(username='admin', password='admin')
		response = self.client.get('')
		self.assertTemplateUsed(response, 'eh_app/index.html')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.context['form'], superuser_filter_form().as_ul())
		self.assertContains(response,"utf-8")

	def test_login_superuser_students(self):
		user = User.objects.create_superuser('admin', 'gg@tt.com', 'admin')
		self.client.login(username='admin', password='admin')
		response = self.client.get('/students')
		self.assertTemplateUsed(response, 'eh_app/student_list.html')
		self.assertEqual(response.status_code, 200)
		self.assertContains(response,"utf-8")

	def test_login_advisor_form(self):
		user = User.objects.create_user('myadmin', 'gg@tt.com', 'password')
		advisor, created = Group.objects.get_or_create(name='Advisor')
		user.groups.add(advisor)
		self.client.login(username='myadmin', password='password')
		response = self.client.get('')
		self.assertTemplateUsed(response, 'eh_app/index.html')
		self.assertEqual(response.context['form'], advisor_filter_form().as_ul())
		self.assertContains(response,"utf-8")

	def test_login_faculty_form(self):
		user = User.objects.create_user('myfac', 'ggg@tt.com', 'password')
		advisor, created = Group.objects.get_or_create(name='Faculty')
		user.groups.add(advisor)
		self.client.login(username='myfac', password='password')
		response = self.client.get('')
		self.assertTemplateUsed(response, 'eh_app/index.html')
		self.assertEqual(response.context['form'], faculty_filter_form().as_ul())
		self.assertContains(response,"utf-8")

class test_studentList(TestCase):
	def test_it(self):
		self.client.login(username='myfac', password='password')
		response = self.client.get('/students')
		request = response.wsgi_request
		studentList(request)
		self.client.login(username='admin', password='admin')
		response = self.client.get('/students')
		request = response.wsgi_request
		studentList(request)
		self.client.login(username='myadmin', password='password')
		response = self.client.get('/students')
		request = response.wsgi_request
		studentList(request)

class CourseTestCase(TestCase):
    fixtures = TEST_SEED_FIXTURES

    def test_parse_course_data(self):
        call_command(
            'parse_courses',
            f'{os.path.join(os.path.dirname(__file__), "..")}/example-parse-data'
        )

class GPAStatusTestCase(TestCase):
    fixtures = ['GPADefAndStatus']

    def test_get_status_queryset(self):
        status = GPAStatus.objects.get_status('D1', 2.6)
        self.assertEqual(status.status, 'Stay on Grace Period-GPA Def')

        status = GPAStatus.objects.get_status('D4', 3.8)
        self.assertEqual(status.status, 'Good Standing(Prev Prob)')

        self.assertIsNone(GPAStatus.objects.get_status('D4', -1))
        self.assertIsNone(GPAStatus.objects.get_status('D10', 2.8))

class SemesterTestCase(TestCase):
    fixtures = TEST_SEED_FIXTURES

    def test_new_current_queryset(self):
        # Where a semester is created newly
        Semester.objects.new_current(id=201921)
        self.assertEqual(Semester.objects.get_current().id, 201921)
        self.assertEqual(Semester.objects.get_current().predecessor.id, 201911)

        # Existing semester is found
        Semester.objects.new_current(id=202211)
        self.assertEqual(Semester.objects.get_current().id, 202211)
        self.assertEqual(Semester.objects.get_current().predecessor.id, 201921)

    def test_past_semester(self):
        sem = Semester.objects.get(id=201831)
        self.assertTrue(sem.is_past())
        self.assertFalse(sem.current)

    def test_is_fall_spring_semester(self):
        sem = Semester.objects.get(id=202211)
        self.assertTrue(sem.is_spring())
        self.assertFalse(sem.is_fall())

        sem = Semester.objects.get(id=201831)
        self.assertTrue(sem.is_fall())
        self.assertFalse(sem.is_spring())

class StudentTestCase(TestCase):
    fixtures = TEST_SEED_FIXTURES

    def test_add_activity_attendance(self):
        call_command(
            'parse_activity_attendance',
            f'{os.path.join(os.path.dirname(__file__), "..")}/example-parse-data'
        )

    def test_add_advising_attendance(self):
        call_command(
            'parse_advising_attendance',
            f'{os.path.join(os.path.dirname(__file__), "..")}/example-parse-data'
        )

    def test_cumulative_gpa(self):
        student = Student.objects.get(uin=218009384)
        self.assertEqual(student.cumulative_gpa(), 4.0)

        student = Student.objects.get(uin=402009991)
        self.assertEqual(student.cumulative_gpa(), 'n/a')

    def test_eh_hours_needed(self):
        student = Student.objects.get(uin=218009384)
        self.assertEqual(student.eh_hours_needed(), 18)

    def test_eh_hours_needed_per_sem(self):
        student = Student.objects.get(uin=218009384)
        self.assertLess(student.eh_hours_needed_per_sem(), 3)

    def test_first_semester(self):
        student = Student.objects.get(uin=358003821)
        self.assertFalse(student.first_semester_eh())

        student = Student.objects.get(uin=329003124)
        self.assertFalse(student.first_semester_eh())

    def test_first_year_grace(self):
        student = Student.objects.get(uin=358003821)
        self.assertTrue(student.first_year_grace())

        student = Student.objects.get(uin=329003124)
        self.assertTrue(student.first_year_grace())

        student = Student.objects.get(uin=987001241)
        self.assertFalse(student.first_year_grace())

        student = Student.objects.get(uin=402009991)
        self.assertEqual(student.first_year_grace(), 'Invalid record')

    def test_major_names(self):
        student = Student.objects.get(uin=218009384)
        self.assertEqual(student.major_names(), ['CPSC'])

        # Test Case 1: change major from CLEN to CSCE
        # student = Student.objects.get(uin=125001293)
        # self.assertEqual(student.major_names(), ['CLEN'])
        student = Student.objects.get(uin=125001293)
        self.assertEqual(student.major_names(), ['CPSC'])

    def test_minor_names(self):
        student = Student.objects.get(uin=218009384)
        self.assertEqual(student.minor_names(), [])

    def test_track(self):
        student = Student.objects.get(uin=218009384)
        self.assertEqual(student.track.code, 6)

        student = Student.objects.get(uin=358003821)
        self.assertEqual(student.track.code, 6)

    # FIXME: Run and fix. Due to lations as statues. Failure in missmatch of all the different codes
    def test_status_gpa_alone(self):

        student = Student.objects.get(uin=218009384)
        self.assertEqual(student.status_gpa_alone().status, 'Stay on Grace Period-GPA Ok')

        # Test Case 2: when GPA goes below 3.5
        # student = Student.objects.get(uin=358003821)
        # self.assertEqual(student.status_gpa_alone().status, 'Stay on Grace Period-GPA Ok')
        student = Student.objects.get(uin=358003821)
        self.assertEqual(student.status_gpa_alone().status, 'Stay on Grace Period-GPA Def')

    def test_status_activity(self):
        student = Student.objects.get(uin=218009384)
        self.assertEqual(student.activity_deficiency_rating(), 'serious')

        student = Student.objects.get(uin=987001241)
        self.assertEqual(student.activity_deficiency_rating(), 'no valid status')

        # TODO: Fill out in testing file
        student = Student.objects.get(uin=358003821)
        self.assertEqual(student.activity_deficiency_rating(), 'serious')

    def test_status_advising(self):
        student = Student.objects.get(uin=218009384)
        self.assertEqual(student.advising_deficiency_rating(), 'on track')

        student = Student.objects.get(uin=987001241)
        self.assertEqual(student.advising_deficiency_rating(), 'no valid status')

        # TODO: Fill out in testing file
        student = Student.objects.get(uin=358003821)
        self.assertEqual(student.advising_deficiency_rating(), 'on track')

    def test_status_annual_report(self):
        student = Student.objects.get(uin=218009384)
        self.assertEqual(student.annual_report_deficiency_rating(), 'on track')

        student = Student.objects.get(uin=987001241)
        self.assertEqual(student.annual_report_deficiency_rating(), 'no valid status')

    def test_status_email_template(self):
        student = Student.objects.get(uin=218009384)
        self.assertEqual(student.status_email_template(), None)

    def test_taken_eh_hours(self):
        student = Student.objects.get(uin=218009384)
        self.assertEqual(student.taken_eh_hours(), 3)

class StudentSectionEnrollmentTestCase(TestCase):
    fixtures = TEST_SEED_FIXTURES

    def test_semester(self):
        student_enrollment = StudentSectionEnrollment.objects.get(id=1)
        self.assertEqual(student_enrollment.semester().semester, 'Spring')
        
        #Test Case 13: Change from Fall to Spring
        # student_enrollment = StudentSectionEnrollment.objects.get(id=4)
        # self.assertEqual(student_enrollment.semester().semester, 'Fall')
        student_enrollment = StudentSectionEnrollment.objects.get(id=4)
        self.assertEqual(student_enrollment.semester().semester, 'Spring')

    def test_current_queryset(self):
        student_enrollment = StudentSectionEnrollment.objects.current(student__uin=218009384)
        self.assertEqual(student_enrollment.get().id, 1)

    def test_credits(self):
        student_enrollment = StudentSectionEnrollment.objects.get(id=1)
        self.assertEqual(student_enrollment.credits(), 3)

class StudentSemesterStatusTestCase(TestCase):
    fixtures = TEST_SEED_FIXTURES

    def test_activity(self):
        #Test Case 4: attending an activity
        # student = StudentSemesterStatus.objects.get(id=5)
        # self.assertEqual(student.activity_deficiency_rating(), 'serious')
        # self.assertEqual(student.activity_attendance(), 1)

        student = StudentSemesterStatus.objects.get(id=5)
        self.assertEqual(student.activity_deficiency_rating(), 'on track')
        self.assertEqual(student.activity_attendance(), 2)

    def test_advising(self):
        # Test Case 5: attending an advising
        # student = StudentSemesterStatus.objects.get(id=5)
        # self.assertEqual(student.advising_deficiency_rating(), 'serious')
        
        student = StudentSemesterStatus.objects.get(id=5)
        self.assertEqual(student.advising_deficiency_rating(), 'on track')

    def test_annual(self):
        #Test Case 6: annual report
        # student = StudentSemesterStatus.objects.get(id=5)
        # self.assertEqual(student.annual_report_deficiency_rating(), 'serious')

        student = StudentSemesterStatus.objects.get(id=5)
        self.assertEqual(student.annual_report_deficiency_rating(), 'on track')

    def test_post_init(self):
        status = StudentSemesterStatus.objects.get(id=1)
        self.assertEqual(status.overall_hours_attempted, 0)
        self.assertEqual(status.final_status.status, 'Good standing-None')
        self.assertEqual(status.previous_final_status.status, 'Good standing-None')

        status = StudentSemesterStatus.objects.get(id=2)
        self.assertEqual(status.hours_attempted, 3)
        self.assertEqual(status.previous_final_status.status, 'Good standing-None')
        self.assertEqual(status.overall_hours_attempted, 3)
        self.assertEqual(status.overall_quality_points, 12)

    def test_finalize_status(self):
        status = StudentSemesterStatus.objects.get(id=1)
        self.assertEqual(status.finalize_status(), 'Spring-GS-GPAOK-PrtcptnOK')

        status = StudentSemesterStatus.objects.get(id=3)
        self.assertEqual(status.finalize_status(), 'Spring-GS-GPAOK-PrtcptnOK')

        status = StudentSemesterStatus.objects.get(id=4)
        self.assertEqual(status.finalize_status(), 'Good Standing')

        # status = StudentSemesterStatus.objects.get(id=6)
        # self.assertEqual(status.finalize_status(), 'Spring-Stay-GPADef-PrtcptnDef')

class EmailTemplateTestCase(TestCase):
    fixtures = TEST_SEED_FIXTURES

    def test_email(self):
        #Test Case 10 and 11: emailTemplate 
        e = EmailTemplate.objects.get(id=1)
        self.assertEqual(e.get_semester(), 'Fall')
        self.assertEqual(e.get_status(), 'Dismiss')
        self.assertEqual(e.get_GPA_status(), 'GPADef')
        self.assertEqual(e.get_part_status(), 'PrtcptnDef')
        self.assertEqual(e.get_response(), None)
        self.assertEqual(e.get_final_status(), 'Dismiss')

        e = EmailTemplate.objects.get(id=10)
        self.assertEqual(e.get_semester(), 'Fall')
        self.assertEqual(e.get_status(), 'Prob')
        self.assertEqual(e.get_GPA_status(), 'GPADef')
        self.assertEqual(e.get_part_status(), 'PrtcptnDef')
        self.assertEqual(e.get_response(), 'Leave')
        self.assertEqual(e.get_final_status(), 'Dismiss')

        e = EmailTemplate.objects.get(id=12)
        self.assertEqual(e.get_semester(), 'Fall')
        self.assertEqual(e.get_status(), 'Prob')
        self.assertEqual(e.get_GPA_status(), 'GPADef')
        self.assertEqual(e.get_part_status(), 'PrtcptnDef')
        self.assertEqual(e.get_response(), 'Stay')
        self.assertEqual(e.get_final_status(), 'Probation')

        # Test Case 7
        # e = EmailTemplate.objects.get(id=36)
        # self.assertEqual(e.get_final_status(), 'Stay')

        # Test Case 8 .
        # e = EmailTemplate.objects.get(id=9)
        # self.assertEqual(e.get_GPA_status(), 'GPAOK')

class viewTestCase(TestCase):
    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
