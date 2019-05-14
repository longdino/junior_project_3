from . import _BaseTimestampModel, EmailTemplate, HonorsCreditHoursRating, GPAAndPartStatus, GPADeficiency, GPAStatus, ParticipationStatus, ProbDefStatus, Semester
from django.db import models
from django.core.exceptions import ObjectDoesNotExist

class Student(_BaseTimestampModel):
    class Meta:
        db_table = 'student'

    uin = models.PositiveIntegerField(primary_key=True)
    netID = models.CharField(max_length=45, default=None, null=True, unique=True)
    first_name = models.CharField(max_length=45, default=None, null=True)
    last_name = models.CharField(max_length=45, default=None, null=True)
    middle_name = models.CharField(max_length=45, default=None, null=True)
    email = models.EmailField(max_length=45, default=None, null=True, unique=True)

    times_on_probation = models.PositiveIntegerField(default=0)
    times_dismissed = models.PositiveIntegerField(default=0)

    # TODO: Should also be set true on turn of semester? Or derived?
    degree_candidate = models.BooleanField(default=False)
    graduated = models.BooleanField(default=False)

    met_track_requirements = models.BooleanField(default=False)
    senior_honors_thesis_completed = models.BooleanField(default=False)
    research_credits = models.PositiveIntegerField(default=0)

    # Relations
    majors = models.ManyToManyField('Major', related_name='majors_set', default=None)
    minors = models.ManyToManyField('Major', related_name='minors_set', default=None)
    track = models.ForeignKey('Track', related_name='track_set', default=None, null=True, on_delete=None)
    first_tamu_semester = models.ForeignKey('Semester', related_name='had_first_tamu_set', default=None, null=True, on_delete=None)
    first_eh_semester = models.ForeignKey('Semester', related_name='had_first_eh_set', default=None, null=True, on_delete=None)
    graduation_semester = models.ForeignKey(
        'Semester',
        related_name='graduating_set',
        default=None,
        null=True,
        on_delete=None,
    )

    def activity_deficiency_rating(self):
        previous_status = self.latest_status()
        if previous_status is None:
            return 'no valid status'

        return previous_status.activity_deficiency_rating()

    def add_activity_attendance(self, activity) -> (bool, str):
        status = self.get_status_by_sem(activity.semester)
        if status:
            status.activities_attended.add(activity)
            return (True, '')
        else:
            return (False, f'Student {self.uin} does not have a semester status element for semester {activity.semester.id}.')

    def add_advising_attendance(self, advising) -> (bool, str):
        status = self.get_status_by_sem(advising.semester)
        if status:
            status.advising_attended.add(advising)
            return (True, '')
        else:
            return (False, f'Student {self.uin} does not have a semester status element for semester {advising.semester.id}.')

    def advising_deficiency_rating(self):
        previous_status = self.latest_status()
        if previous_status is None:
            return 'no valid status'

        return previous_status.advising_deficiency_rating()

    def annual_report_deficiency_rating(self):
        previous_status = self.latest_status()
        if previous_status is None:
            return 'no valid status'

        return previous_status.annual_report_deficiency_rating()

    # Taken from all previous semesters
    # From student semester status set.last
    def cumulative_gpa(self):
        previous_status = self.latest_status()
        if not previous_status:
            return 'n/a'

        return float(previous_status.overall_gpa)

    def eh_hours_needed(self):
        #FIXME: Add a default track_enrollment?
        return self.track.hours_required() - self.taken_eh_hours()

    def eh_hours_needed_per_sem(self):
        sem_left = self.tamu_semesters_left()
        if sem_left == 0:
            return self.eh_hours_needed()
        else:
            return self.eh_hours_needed() / sem_left

    def eh_hours_rating(self):
        if self.first_eh_semester.id == Semester.objects.get_current().id:
            return 'on track'

        return HonorsCreditHoursRating.objects.get_rating(
            self.eh_hours_needed_per_sem()
        ).rating

    def first_semester_eh(self):
        return self.first_eh_semester.id == Semester.objects.get_current().id

    def first_year_grace(self):
        current_sem = Semester.objects.get_current()

        temp = self.first_tamu_semester
        for i in range(3):
            if temp.id == current_sem.id:
                return True
            elif temp.successor:
                temp = temp.successor
            else:
                return 'Invalid record'

        return False

    def latest_status(self):
        return self.semester_statuses_set.last()

    def latest_finalized_status(self):
        return self.semester_statuses_set \
            .filter(finalized=True) \
            .order_by('-semester__id') \
            .first()

    def get_season(self):
        current_semester = Semester.objects.get_current()
        if current_semester.is_spring():
            return 'Spring'
        else:
            return 'Fall'

    def major_names(self):
        major_names = []
        majors = self.majors.all()
        for major in majors:
            major_names.append(major.name)

        return major_names

    def minor_names(self):
        minor_names = []
        minors = self.minors.all()
        for minor in minors:
            minor_names.append(minor.name)

        return minor_names

    def get_status_by_sem(self, semester):
        try:
            return self.semester_statuses_set.get(
                semester__id=semester.id
            )
        except ObjectDoesNotExist:
            return None

     # Test for emailTemplate
    def status_email_template(self):
        last_status = self.latest_status()
        if not last_status:
            return 'N/A'

        return EmailTemplate.objects.get_status(
            last_status.status
        )

    def status_gpa_alone(self):
        last_status = self.latest_status()
        if not last_status:
            return 'n/a'

        deficiency_value_prefix = 'Y-' if self.first_year_grace() else 'N-'
        print(last_status.previous_final_status.gpa_status)
       # print(deficiency_value_prefix + last_status.previous_final_status.gpa_status)
        deficiency = GPADeficiency.objects.get(
            value=deficiency_value_prefix + last_status.previous_final_status.gpa_status
        )

        return GPAStatus.objects.get_status(
            deficiency.code,
            float(last_status.overall_gpa),
        )

    #TODO: Test once status on participation is finalized
    def status_gpa_and_part(self):
        print(self.status_gpa_alone().status)
        print(self.status_part_alone().status)
        return GPAAndPartStatus.objects.get_status(
            self.status_gpa_alone().status,
            self.status_part_alone().status,
        )

    def status_part_alone(self):
        return ParticipationStatus.objects.get_recommendation(
            self.get_season().lower(),
            self.eh_hours_rating(),
            self.activity_deficiency_rating(),
            self.annual_report_deficiency_rating(),
            self.advising_deficiency_rating(),
        )

    def status_prob_def(self):
        last_status = self.latest_status()
        if not last_status:
            return 'N/A'

        return ProbDefStatus.objects.get_status(
            self.status_gpa_alone().status,
            self.cumulative_gpa()
        )

    # This includes current and pre-reg
    def taken_eh_hours(self):
        sum = 0
        for enrollment in self.enrolled_section_set.all():
            if not enrollment.is_eh():
                continue

            sum += enrollment.credits()
        return sum
    # Based of off config page
    # Semester left simplified
    def tamu_semesters_left(self):
        distance = Semester.objects.distance_from(self.first_tamu_semester)
        if distance == 0 or distance < 8:
            return (8 - distance) - 1
        else:
            return 0

    def track_requirements(self):
        return self.track_enrollment.track.requirements

    # Overrides
    # Override of save enforces validate_unique so uniqueness of relations can be established
    # No test on django pure code
    def save(self, *args, **kwargs): # pragma: no cover
        super(Student, self).validate_unique(*args, **kwargs)
        super(Student, self).save(*args, **kwargs)
