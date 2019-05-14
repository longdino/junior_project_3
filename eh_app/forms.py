from django import forms
SUPERUSER_CATEGORY_FILTER_OPTIONS = [('first_name','First Name'),('last_name','Last Name'),('middle_name','Middle Name'),('email','Email'),('cumulative_gpa','GPA'),
	('status_gpa_alone','Status Based on GPA Alone'),('times_on_probation','Times on Probation'),
	('first_year_grace','First Year Grace?'),('times_dismissed','Times Dismissed'),
	('major_names','Major(s)'),('minor_names','Minor(s)'),('degree_candidate','Degree Candidate?'),
	('graduated','Graduated?'),('first_eh_semester','First EH Semester'),('first_tamu_semester','Start Semester'),('tamu_semesters_left','Semesters Left'),('graduation_semester','Graduation Semester'),
	('advising_deficiency_rating','Advising Deficiency Rating'),('activity_deficiency_rating','Activity Deficiency Rating'),('annual_report_deficiency_rating','Annual Report Deficiency Rating'),
	('status_part_alone','Participation Status'),('taken_eh_hours','Taken EH Hours'),('eh_hours_needed','Total EH Hours Needed'),('eh_hours_needed_per_sem','EH Hours Needed Per Semester'),
	('eh_hours_rating','EH_Hours Deficiency Rating'),('status_gpa_and_part','Round 1 Status'),('student_feedback','Student Response'),('round_two_status','Round 2 Status'),
	('improvement_plan_complete','Improvement Plan Complete?'),('improvement_plan_approval','Improvement Plan Approved?'),
	('round_three_status','Round 3 Status'),('tc_feedback','Advisor Feedback'),('tc_feedback_override','Override Final Ruling with Advisor Feedback?'),('get_final_status','Final Status')]
SEMESTER_STATUS_CATEGORIES = [('student_feedback','Student Response')]
FACULTY_CATEGORY_FILTER_OPTIONS = [('first_name','First Name'),('last_name','Last Name'),('middle_name','Middle Name'),('uin','UIN'),('email','Email'),('times_on_probation','Times on Probation'),
	('times_dismissed','Times Dismissed'),('cumulative_gpa','GPA'),('first_year_grace','First Year Grace?'),
	('status_gpa_alone','Status Based on GPA Alone'),('degree_candidate','Degree Candidate?'),
	('graduated','Graduated?'),('major_names','Major(s)'),('minor_names','Minor(s)'),('first_tamu_semester','Start Semester'),('graduation_semester','Graduation Semester'),
	('first_eh_semester','First EH Semester'),
	('advising_deficiency_rating','Advising Deficiency Rating'),('annual_report_deficiency_rating','Annual Report Deficiency Rating'),
	('eh_hours_needed','Total EH Hours Needed'),('eh_hours_needed_per_sem','EH Hours Needed Per Semester'),('eh_hours_rating','EH_Hours Deficiency Rating'),('status_gpa_and_part','Total Status'),
	('taken_eh_hours','Taken EH Hours')]
ADVISOR_CATEGORY_FILTER_OPTIONS = [('first_name','First Name'),('last_name','Last Name'),('middle_name','Middle Name'),('uin','UIN'),('email','Email'),('times_on_probation','Times on Probation'),
	('times_dismissed','Times Dismissed'),('first_year_grace','First Year Grace?'),
	('status_gpa_alone','Status Based on GPA Alone'),('degree_candidate','Degree Candidate?'),
	('graduated','Graduated?'),('major_names','Major(s)'),('minor_names','Minor(s)'),('first_tamu_semester','Start Semester'),('graduation_semester','Graduation Semester'),
	('first_eh_semester','First EH Semester'),
	('advising_deficiency_rating','Advising Deficiency Rating'),('annual_report_deficiency_rating','Annual Report Deficiency Rating'),
	('eh_hours_needed','Total EH Hours Needed'),('eh_hours_needed_per_sem','EH Hours Needed Per Semester'),('eh_hours_rating','EH_Hours Deficiency Rating'),('status_gpa_and_part','Total Status'),
	('taken_eh_hours','Taken EH Hours'),('tamu_semesters_left','Semesters Left')]
STUDENT_FILTER_OPTIONS = [('*','All Students'),("gpal3.5",'Students with less than a 3.5 GPA'),("{'first_name':'Henry'}","First Name Henry")]
#('activities_attended','Activities Attended'),('activity_attendance_deficiency_rating','Activity Attendance Deficiency Rating'),('status_participation_alone','Status Based on Participation Alone'),
class superuser_filter_form(forms.Form):
	category_filter = forms.MultipleChoiceField(
		required=True,
		widget=forms.CheckboxSelectMultiple(attrs={'class':'filter_options'}),
		choices=SUPERUSER_CATEGORY_FILTER_OPTIONS,
		label="Category Filters",)
	student_filter = forms.ChoiceField(
		choices=STUDENT_FILTER_OPTIONS,
		label="Student Filters",
		)
class faculty_filter_form(forms.Form):
	category_filter = forms.MultipleChoiceField(
		required=True,
		widget=forms.CheckboxSelectMultiple(attrs={'class':'filter_options'}),
		choices=FACULTY_CATEGORY_FILTER_OPTIONS,
		label="Category Filters",)
	student_filter = forms.ChoiceField(
		choices=STUDENT_FILTER_OPTIONS,
		label="Student Filters",
		)
class advisor_filter_form(forms.Form):
	category_filter = forms.MultipleChoiceField(
		required=True,
		widget=forms.CheckboxSelectMultiple(attrs={'class':'filter_options'}),
		choices=ADVISOR_CATEGORY_FILTER_OPTIONS,
		label="Category Filters",)
	student_filter = forms.ChoiceField(
		choices=STUDENT_FILTER_OPTIONS,
		label="Student Filters",
		)