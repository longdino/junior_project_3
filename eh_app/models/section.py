from . import _BaseTimestampModel
from django.db import models

class Section(_BaseTimestampModel):
    class Meta:
        db_table = 'section'
        unique_together = (('crn', 'semester', 'campus'),)

    LEVEL_CHOICES = (
        ('UG', 'Undergrad'),
        ('GR', 'Graduate'),
        ('NC', 'NC'),   # FIXME: Not sure what the nc field is
    )

    #id autogen
    crn = models.CharField(max_length=16)
    number = models.PositiveIntegerField(default=None, null=True)
    level = models.CharField(
        max_length=20,
        choices=LEVEL_CHOICES,
        null=True
    )
    eh = models.BooleanField(default=False)

    # Relations
    course = models.ForeignKey('Course', on_delete=None)
    teachers = models.ManyToManyField('Teacher', related_name='sections_set')
    semester = models.ForeignKey('Semester', on_delete=None)
    campus = models.ForeignKey('Campus', default=None, null=True, on_delete=None)

    def credits(self): # pragma: no cover
        return self.course.credits

    # Overrides
    # Override of save enforces validate_unique so uniqueness of relations can be established
    def save(self, *args, **kwargs): # pragma: no cover
        super(Section, self).validate_unique(*args, **kwargs)
        super(Section, self).save(*args, **kwargs)
