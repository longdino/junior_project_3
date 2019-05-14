from django.db import models
from .custom_signals import semester_change

class EmailTemplateQueryset(models.QuerySet):
    def get_status(self, response):
        status_elems = self.filter(
            response = response,
        )
        if len(status_elems):
            return status_elems.last()
        else:
            return None

class GPAAndPartStatusQueryset(models.QuerySet):
    def get_status(self,
        gpa_status,
        participation_status,
    ):
        status_elems = self.filter(
            gpa_status=gpa_status,
            participation_status=participation_status,
        )

        if len(status_elems):
            return status_elems.last()
        else:
            return None

    def get_statuses_list(self):
        return list(set([status.status for status in self.all()]))

class GPAStatusQueryset(models.QuerySet):
    def get_status(self, code, max_gpa):
        status_elems = self.filter(code=code, max_gpa__lte=max_gpa).order_by('max_gpa')

        if len(status_elems):
            return status_elems.last()
        else:
            return None

class HonorsCreditHoursRatingQueryset(models.QuerySet):
    def get_rating(self, hours_needed_per_sem):
        rating_elems = self.filter(hours_needed_per_sem__gte=hours_needed_per_sem)

        if len(rating_elems):
            return rating_elems.first()
        else:
            return None

class ParticipationStatusQueryset(models.QuerySet):
    def get_recommendation(
        self,
        season,
        honors_credit_rating,
        activity_requirement_rating,
        annual_report_rating,
        advising_requirement_rating,
    ):
        rating_elems = self.filter(
            season=season,
            honors_credit_rating=honors_credit_rating,
            activity_requirement_rating=activity_requirement_rating,
            annual_report_rating=annual_report_rating,
            advising_requirement_rating=advising_requirement_rating
        )

        if len(rating_elems):
            return rating_elems.first()
        else:
            print("Lame " + str(season))
            return None

class ProbAndGPADefQueryset(models.QuerySet):
    def get_status(self, gpa_status, max_gpa):
        status_elems = self.filter(gpa_status=gpa_status, max_gpa__lte=gpa).order_by('max_gpa')

        if len(status_elems):
            return status_elems.last()
        else:
            return None

class SemesterQueryset(models.QuerySet):
    def current(self):
        return self.filter(current=True)

    #FIXME: Does this really work?
    def distance_from(self, from_semester):
        current = self.get_current()
        distance = 0

        while current.predecessor:
            if current.id == from_semester.id:
                return distance

            current = current.predecessor

        return -1

    def new_current(self, *args, **kwargs):
        new_current, created = self.get_or_create(*args, **kwargs)

        current = self.get_current()
        semester_change.send_robust(sender=self.model, old_current_sem=current)

        if created:
            current.successor = new_current
            current.current = False
            current.save()

        new_current.current = True
        new_current.save()

        return new_current

    def get_current(self):
        return self.current().get()

class StudentSectionEnrollmentQueryset(models.QuerySet):
    def current(self, *args, **kwargs):
        return self.filter(section__semester__current=True, *args, **kwargs)
