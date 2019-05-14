from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Semester, StudentSectionEnrollment, StudentSemesterStatus
from .custom_signals import semester_change

# NOTE: There should be a check to see if the student has graduated before creating a new semester status
@receiver(post_save, sender=StudentSemesterStatus)
def fill_in_overall_fields(sender, instance, created, raw, *args, **kwargs):
    if (created or raw) and instance.predecessor:
        prd = instance.predecessor
        print("SemesterStatusSavedFromSignal")
        instance.overall_hours_attempted = prd.overall_hours_attempted + prd.hours_attempted
        instance.overall_hours_earned = prd.overall_hours_earned + prd.hours_earned
        instance.overall_hours_passed = prd.overall_hours_passed + prd.hours_passed
        instance.overall_quality_points = prd.overall_quality_points + prd.quality_points
        instance.overall_gpa = prd.overall_gpa + prd.semester_gpa
        instance.previous_final_status = prd.status()

        instance.save()

@receiver(semester_change, sender=Semester)
def finalize_semester_statuses(sender, old_current_sem, *args, **kwargs):
    to_finalize = StudentSemesterStatus.objects.filter(semester=old_current_sem)

    for status in to_finalize:
        section_enrollments = status.relevant_section_enrollments()

        # Getting grades, points, etc. given tamu grading distribution
        # TODO: This may need tweaking based on track grade reqs. (e.g., 'C' or better for MATH 251)
        for section_enrollment in section_enrollments:
            if not section_enrollment.valid:
                # FIXME: Perhaps flashing a message to the user instead? Or blocking action?
                # Should this fail?
                print(
                    f"""
                    A section enrollment was invalid. This enrollment is being skipped:
                    Section id:{section_enrollment.section.id}
                    Student uin:{section_enrollment.student.uin}
                    """
                )
                continue

            hours_attempted = section_enrollment.credits()
            if section_enrollment.grade:
                grade = section_enrollment.grade.upper()
                if grade in ['A', 'B', 'C', 'D', 'F', 'F*']:
                    status.hours_attempted += hours_attempted
                if grade in ['A', 'B', 'C', 'D']:
                    status.hours_earned += hours_attempted
                    status.hours_passed += hours_attempted

                if grade == 'A':
                    status.quality_points += hours_attempted * 4
                if grade == 'B':
                    status.quality_points += hours_attempted * 3
                if grade == 'C':
                    status.quality_points += hours_attempted * 2
                if grade == 'D':
                    status.quality_points += hours_attempted * 1

            elif section_enrollment.grading_mode and section_enrollment.grading_mode.upper() == 'U':
                status.hours_attempted += hours_attempted

        status.semester_gpa = status.quality_points / status.hours_attempted

        # Establishing status relations
        status.gpa_alone_status = status.student.status_gpa_alone()
        status.prob_def_status = status.student.status_prob_def()
        status.part_alone_status = status.student.status_part_alone()
        status.init_combined_status = status.student.status_gpa_and_part()
        status.email_template_status = status.student.status_email_template()

        status.save()

        StudentSemesterStatus.objects.create(predecessor=status)
