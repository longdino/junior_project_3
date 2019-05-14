from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from .forms import advisor_filter_form,ADVISOR_CATEGORY_FILTER_OPTIONS,faculty_filter_form,FACULTY_CATEGORY_FILTER_OPTIONS,superuser_filter_form,SEMESTER_STATUS_CATEGORIES,SUPERUSER_CATEGORY_FILTER_OPTIONS,STUDENT_FILTER_OPTIONS
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
import yaml
import os
import ast
# Create your views here.


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEED_DIR = os.path.join(BASE_DIR, "eh_app", "fixtures", "test_seed.yaml")

#Render of the index page
#Either login or selection of filters for student list
def index(request):
	#Not sure what this is for
	with open(SEED_DIR, 'r') as stream:
		
		data = yaml.load(stream)
			#print(data)

	#Filter Form Rendering
	form = ''
	if request.user.is_superuser:
		form = superuser_filter_form().as_ul()
	elif request.user.groups.filter(name='Advisor').exists():
		form = advisor_filter_form().as_ul()
	elif request.user.groups.filter(name='Faculty').exists():
		form = faculty_filter_form().as_ul()
	else:
		form = superuser_filter_form().as_ul()
	return render(request, 'eh_app/index.html', {'form':form})
def override_final(request):
	if request.method == "POST":
		filters = request.POST
		UIN = filters["UIN"]
		value = filters["value"]
		print("gggggg")
		print(filters)
		print(value)
		students = Student.objects.filter(uin=UIN)
		student = students[0]
		print(student)
		currentSemester = student.latest_status()
		currentSemester.tc_feedback_override(value,True)
	return index(request)
#Render of the page that lists students and their info
@never_cache
def studentList(request):
	category_filters = []
	student_filters = []
	raw_filters = []
	students = Student.objects.filter()
	self_filter = False
	
	if request.user.groups.filter(name='Advisor').exists():
		CATEGORY_FILTER_OPTIONS = ADVISOR_CATEGORY_FILTER_OPTIONS
	if request.user.groups.filter(name='Faculty').exists():
		CATEGORY_FILTER_OPTIONS = FACULTY_CATEGORY_FILTER_OPTIONS
	if request.user.is_superuser:
		CATEGORY_FILTER_OPTIONS = SUPERUSER_CATEGORY_FILTER_OPTIONS
	if not request.user.is_superuser and not request.user.groups.filter(name='Faculty').exists() and not request.user.groups.filter(name='Advisor').exists():
		CATEGORY_FILTER_OPTIONS = []
	if request.method == "POST":
		filters = request.POST
		category_filters = filters.getlist('category_filter')
		if len(category_filters) == 0:
			return render(request, 'eh_app/student_list.html')
		category_iterator = 0

		student_filters = filters.getlist('student_filter')
		if student_filters[0] != '*':
			try:
				args = ast.literal_eval(student_filters[0])
				students = Student.objects.filter(**args)
			except:
				self_filter = True

		studentResults = []
		
		for student in students:
			if self_filter:
				if student_filters[0] == "gpal3.5":
					if student.cumulative_gpa() != 'n/a' and float(student.cumulative_gpa()) >= 3.5:
						continue
			studentDict = dict()
			studentDict["UIN"] = student.uin
			for category in category_filters:
				try:
					methodOrVar = getattr(student,category)
				except:
					try:
						methodOrVar = getattr(student.latest_status(),category)
						#print(methodOrVar)
					except BaseException as e:
						methodOrVar = ""#str(e)
				if callable(methodOrVar):
					try:
						result = methodOrVar()
						#	result = result.status
					except BaseException as e:
						result = ""#str(e)
				else:
					result = methodOrVar
				if isinstance(result,GPAStatus):
					result = result.status
				elif isinstance(result,Semester):
					result = result.semester + " " + result.academic_year
				elif isinstance(result,ParticipationStatus):
					result = result.status
				elif isinstance(result,GPAAndPartStatus):
					result = result.status
				elif category == "tc_feedback":
					result = "&" + str(result)
				elif category == "tc_feedback_override":
					result = "*^^"
				#elif isinstance(result,StudentSemesterStatus):
				#	
				#	for pair in SEMESTER_STATUS_CATEGORIES:
				#		if category == pair[1]:
				#			print("HHHHHHH")
				#			methodOrVar = getattr(result,pair[0])
				#			if callable(methodOrVar):
				#				try:
				#					result = methodOrVar()
						#	result = result.status
				#				except BaseException as e:
				#					result = str(e)
				#			else:
				#				result = methodOrVar
				studentDict[category] = result
			studentResults.append(studentDict)
		students = studentResults#Student.objects.values(*category_filters)

		for obj in CATEGORY_FILTER_OPTIONS:
			if category_filters[category_iterator] == obj[0]:
				category_filters[category_iterator] = obj[1]
				category_iterator += 1
			if category_iterator == len(category_filters):
				break

		category_filters.insert(0,"UIN")
	else:
		for obj in CATEGORY_FILTER_OPTIONS:
			category_filters.append(obj[1])
			raw_filters.append(obj[0])
		category_filters.insert(0,"UIN")
		studentResults = []
		for student in students:
			studentDict = dict()
			studentDict["UIN"] = student.uin
			for category in raw_filters:
				try:
					methodOrVar = getattr(student,category)
				except:
					try:
						methodOrVar = getattr(student.latest_status(),category)
						#print(methodOrVar)
					except BaseException as e:
						methodOrVar = ""#str(e)
				if callable(methodOrVar):
					try:
						result = methodOrVar()
					except BaseException as e:
						result = ""#str(e)
				else:
					result = methodOrVar
				if isinstance(result,GPAStatus):
					result = result.status
				elif isinstance(result,Semester):
					result = result.semester + " " + result.academic_year
				elif isinstance(result,ParticipationStatus):
					result = result.status
				elif isinstance(result,GPAAndPartStatus):
					result = result.status
				elif category == "tc_feedback":
					result = "&" + str(result)
				elif category == "tc_feedback_override":
					result = "*^^"
				studentDict[category] = result
			studentResults.append(studentDict)
		students = studentResults
	return render(request, 'eh_app/student_list.html', {'category_filters':category_filters,'students': students})
