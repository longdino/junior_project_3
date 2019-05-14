from . import _BaseTimestampModel
from ..querysets import GPAAndPartStatusQueryset
from django.db import models

class GPAAndPartStatus(_BaseTimestampModel):
    class Meta:
        db_table = 'gpa_and_part_deficiency'
        unique_together = (('gpa_status', 'participation_status'),)

    #id autogen
    gpa_status = models.CharField(max_length=40)
    participation_status = models.CharField(max_length=45)
    status = models.CharField(max_length=62)

    objects = GPAAndPartStatusQueryset.as_manager()

    # FIXME: This seems like a crude solution. How can this be avoided?
    # Perhaps this system needs to be refined (cohort included)
    # def lookup_for_gpa_status(self):
    #     statuses = self.objects.get_statuses_list()
