from . import _BaseTimestampModel
from ..querysets import SemesterQueryset
from django.db import models

class Semester(_BaseTimestampModel):
    class Meta:
        db_table = 'semester'

    id = models.PositiveIntegerField(primary_key=True)
    semester = models.CharField(max_length=16, default=None, null=True)
    academic_year = models.CharField(max_length=9, default=None, null=True)
    current = models.BooleanField(default=False)

    # Relations
    successor = models.OneToOneField(
        'self',
        related_name='predecessor',
        default=None,
        null=True,
        on_delete=None
    )

    objects = SemesterQueryset.as_manager()

    # Is contained in semester chain and is less than current semester
    def is_past(self):
        return self.successor and self.id < Semester.objects.get_current().id

    # 5th digit is spring/summer/fall signifier 1/2/3 resp.
    def is_spring(self):
        sem_val = str(self.id)[-2]
        return True if sem_val == "1" else False

    def is_fall(self):
        sem_val = str(self.id)[-2]
        return True if sem_val == "3" else False
