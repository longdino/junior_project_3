from . import _BaseTimestampModel, GPAStatus, GPAAndPartStatus, ParticipationStatus, Semester, emailTemplate
from django.db import models

# Finalized for each student on the turn of a semester
# History element to track eh status by semester
# All null fields and overalls will be finalized when the semester is changed
class StudentSemesterStatus(_BaseTimestampModel):
    class Meta:
        db_table = 'student_semester_status'
        unique_together = (('semester', 'student', 'predecessor',),)

    # id autogen
    # Performance of this semester alone
    hours_attempted = models.PositiveIntegerField()
    hours_earned = models.PositiveIntegerField(default=0)
    hours_passed = models.PositiveIntegerField(default=0)
    quality_points = models.PositiveIntegerField(default=0)
    semester_gpa = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    # FIXME: Need count based off of requirements satisfied in both cases
    # FIXME: Needs integration into the logic below
    # Should there even be a requirement, activity, advising table is the data is an int from ecampus?
    activities_attended = models.ManyToManyField('Activity', related_name='activities_attendance_set')
    advising_attended = models.ManyToManyField('StudentAdvisorMeeting', related_name='advising_attendance_set')

    # FIXME: Additional fields added must be verified and during finalization
    # Annual Metrics
    ANNUAL_REPORT_CHOICES = (
        ('on track', 'on track'),
        ('approve', 'approve'),
        ('complete', 'complete'),
        ('serious', 'serious'),
    )
    annual_report = models.CharField(max_length=16, choices=ANNUAL_REPORT_CHOICES, default='on track')
    annual_report_complete = models.BooleanField(default=False)
    # Options: 'approved', 'disapproved', 'pending'
    IMPROVEMENT_PLAN_APPROVAL_CHOICES = (
        ('approved', 'approved'),
        ('disapproved', 'disapproved'),
        ('pending', 'pending'),
    )
    improvement_plan_approval = models.CharField(max_length=16, choices=IMPROVEMENT_PLAN_APPROVAL_CHOICES, default='pending')
    improvement_plan_complete = models.BooleanField(default=False)

    # Based off of previous semesters, doesn't include fields above unless finalized == true
    # Initially just a pull from the previous semester status
    finalized = models.BooleanField(default=False)
    overall_hours_attempted = models.PositiveIntegerField(default=0)
    overall_hours_earned = models.PositiveIntegerField(default=0)
    overall_hours_passed = models.PositiveIntegerField(default=0)
    overall_quality_points = models.PositiveIntegerField(default=0)
    overall_gpa = models.DecimalField(max_digits=3, decimal_places=2, default=0)

    # Relations
    student = models.ForeignKey(
        'Student',
        related_name='semester_statuses_set',
        on_delete=None,
    )
    semester = models.ForeignKey('Semester', on_delete=None)
    predecessor = models.OneToOneField(
        'self',
        related_name='successor',
        default=None,
        null=True,
        on_delete=None
    )
    student_exception = models.ForeignKey(
        'StudentException',
        related_name='semesters_excepted_set',
        default=None,
        null=True,
        on_delete=None
    )

    # Status elements from here on
    tc_feedback = models.TextField(default=None, null=True) # Should be coupled with the tc selecting the final status manually
    student_feedback = models.TextField(default="", null=True)
    tc_overrode_final = models.BooleanField(default=False) # Track whether the tc overwrote the final with value other than the initially suggested
    admin_enforced_init_on_final = models.BooleanField(default=False) # Tracks if admin selects field to override tc_selection with the initial status
    email_round = models.PositiveIntegerField(default=1)

    # Relations
    # Finalized with signal
    GPA_ALONE_STATUS_DEFAULT = 21
    # Field AN
    gpa_alone_status = models.ForeignKey(   # default='n/a'
        'GPAStatus',
        related_name='gpa_alone_statuses_set',
        default=GPA_ALONE_STATUS_DEFAULT, # Relates to pk in the GPAStatus.yaml fixture, as do the following defaults
        on_delete=None
    )
    # Field AM
    PROB_DEF_STATUS_DEFAULT = 1
    prob_def_status = models.ForeignKey(
        'ProbDefStatus',
        related_name='prob_def_statuses_set',
        default=PROB_DEF_STATUS_DEFAULT,
        on_delete=None
    )
    # Field BC
    PART_ALONE_STATUS_DEFAULT = 81
    part_alone_status = models.ForeignKey(  # default='n/a'
        'ParticipationStatus',
        related_name='part_alone_statuses_set',
        default=PART_ALONE_STATUS_DEFAULT,
        on_delete=None
    )
    # Field BD
    INIT_FINAL_STATUS_DEFAULT = 29
    init_combined_status = models.ForeignKey(   # default='n/a'
        'GPAAndPartStatus',
        related_name='init_combined_statuses_set',
        default=INIT_FINAL_STATUS_DEFAULT,
        on_delete=None
    )
    # Field BL
    EMAIL_STATUS_DEFAULT = 71
    email_template_status = models.ForeignKey(
        'EmailTemplate',
        related_name= 'email_template_set',
        default=EMAIL_STATUS_DEFAULT,
        null=True,
        on_delete=None
    )
    # Field DJ
    final_status = models.ForeignKey(   # default='n/a'
        'GPAAndPartStatus',
        related_name='final_statuses_set',
        default=INIT_FINAL_STATUS_DEFAULT,
        on_delete=None
    )
    PREVIOUS_FINAL_STATUS_DEFAULT = 27
    previous_final_status = models.ForeignKey(  # default='Good standing-None'
        'GPAAndPartStatus',
        related_name='previous_final_statuses_set',
        default=PREVIOUS_FINAL_STATUS_DEFAULT,
        on_delete=None
    )

    def activity_attendance(self):
        return self.activities_attended.count()

    def activity_deficiency_rating(self):
        student_track = self.student_track()
        if student_track is None:
            return 'no student track/track enrollment'

        current_sem = Semester.objects.get_current()
        per_sem_req = student_track.activities_per_sem()

        # Consulting the exception requirements if present
        if self.student_exception:
            per_sem_req = self.student_exception.activities_per_sem()

        if self.activity_attendance() >= per_sem_req:
            return 'on track'
        else:
            if current_sem.is_spring():
                return 'serious'
            else:
                if per_sem_req - self.activity_attendance() <= 1:
                    return 'minor'
                else:
                    return 'serious'
        #testing

    def admin_enforce_init_on_final(self):
        self.final_status = self.init_combined_status
        self.admin_enforced_init_on_final = True

        self.save()

    def advising_attendance(self):
        return self.advising_attended.count()

    def advising_deficiency_rating(self):
        student_track = self.student_track()
        if student_track is None:
            return 'no student track/track enrollment'

        current_sem = Semester.objects.get_current()
        per_sem_req = student_track.advising_per_sem()

        # Consulting the exception requirements if present
        if self.student_exception:
            per_sem_req = self.student_exception.advising_per_sem()

        if self.advising_attendance() >= per_sem_req:
            return 'on track'
        else:
            if current_sem.is_spring():
                return 'serious'
            else:
                if per_sem_req - self.advising_attendance() < 1:
                    return 'minor'
                else:
                    return 'serious'

    def annual_report_deficiency_rating(self):
        current_sem = Semester.objects.get_current()
        if current_sem.is_spring():
            if (
                (self.annual_report == 'complete') or
                (self.annual_report == 'approve') or
                (self.annual_report == 'on track')
            ):
                return 'on track'
            else:
                return 'serious'
        else:
            return 'on track'

    def relevant_section_enrollments(self):
        return self.student.enrolled_section_set.filter(semester__id=self.semester.id)

    # Gives the current status elem (most up to date) or None at all if all are defaults
    def status(self):
        if self.finalized:
            return self.final_status

        if self.init_combined_status.id != self.INIT_FINAL_STATUS_DEFAULT:
            return self.init_combined_status
        elif self.part_alone_status.id != self.PART_ALONE_STATUS_DEFAULT:
            return self.part_alone_status
        elif self.gpa_alone_status.id != self.GPA_ALONE_STATUS_DEFAULT:
            return self.gpa_alone_status
        elif self.email_template_status.id != self.EMAIL_STATUS_DEFAULT:
            return self.email_template_status
	#FUTURE: does not incorporate student response, it should
    def round_two_status(self):
        return self.student.status_gpa_and_part()
    def round_three_status(self):
        status = self.email_template_status.get_final_status()
        if status == 'Good Standing' or 'Dismiss':
            return status
        elif status == 'Probation' and self.improvement_plan_complete and self.improvement_plan_approval == 'approved':
            return 'Stay'
        elif status == 'Probation' and self.improvement_plan_complete and self.improvement_plan_approval == 'disapproved':
            return 'Dismiss'
        elif status == 'Probation' and not self.improvement_plan_complete :
            return 'Dismiss'
    def get_final_status(self):
        print(self.tc_feedback)
        if self.tc_overrode_final:
            return self.tc_feedback
        return self.round_three_status()
    def student_track(self):
        try:
            return self.student.track
        except:
            return None

    def set_student_feedback(self, feedback):
        self.student_feedback = feedback

        self.save()
    def tc_feedback_override(self, tc_feedback, override_value=None):
        self.tc_feedback = tc_feedback
		
        if override_value and not self.admin_enforced_init_on_final:
        #self.final_status = override_value
            self.tc_overrode_final = True

        self.save()
    def student_email_round(self, stage):
        self.student_email_round = stage

        self.save()

     #TODO: need to be confirmed.
    def finalize_status(self):
        stage = self.email_round
        feedback = self.student_feedback
        status = self.email_template_status.get_final_status()
        #if student response n/a, then stage is 1 (1st round)
        #if student response received, then stage is 2 (2nd round)
        #if student submitted improvement plan, then tsge is 3 (final round)
        if stage == 1:
            if feedback is None:
                return self.email_template_status.resopnse
            else:
                stage = self.student_email_round(2)
                return self.email_template_status.response
        elif stage == 2:
            stage = self.student_email_round(3)
            return self.email_template_status.response
        elif stage == 3:
            if status == 'Good Standing' or 'Dismiss':
                return status
            elif status == 'Probation' and self.improvement_plan_complete \
                    and self.improvement_plan_approval == 'approved':
                return 'Stay'
            elif status == 'Probation' and self.improvement_plan_complete \
                    and self.improvement_plan_approval == 'disapproved':
                return 'Dismiss'
            elif status == 'Probation' and not self.improvement_plan_complete :
                return 'Dismiss'

    # Overrides
    # Override of save enforces validate_unique so uniqueness of relations can be established
    def save(self, *args, **kwargs): # pragma: no cover
        super(StudentSemesterStatus, self).validate_unique(*args, **kwargs)
        super(StudentSemesterStatus, self).save(*args, **kwargs)
