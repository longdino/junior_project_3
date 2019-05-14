from . import _BaseTimestampModel
from ..querysets import EmailTemplateQueryset
from django.db import models

# Produce a final status of the student
# All null fields and overalls will be finalized whenthe semester is changed
class EmailTemplate(_BaseTimestampModel):
    class Meta:
        db_table = 'email_template'

    # id autogen
    # table from the email template
    # Options: 'leave', 'stay'
    STUDENT_RESPONSE_CHOICES = (
        ('Leave', 'Leave'),
        ('Stay', 'Stay')
    )
    response = models.CharField(max_length=45, choices=STUDENT_RESPONSE_CHOICES, default=None, null=True)
    default_status = models.CharField(max_length=16, default=None, null=True)

    objects = EmailTemplateQueryset.as_manager()

    # Break down the one string that is a concat of possible outcomes
    # From the table EH tab under BL
    def split_table(self):
        s = str(self.response)
        splited_s = s.split("-")
        return splited_s

    def get_semester(self):
        list = self.split_table()
        return list[0]

    def get_status(self):
        list = self.split_table()
        return list[1]

    def get_GPA_status(self):
        list = self.split_table()
        return list[2]

    def get_part_status(self):
        list = self.split_table()
        return list[3]

    def get_response(self):
        list = self.split_table()
        print(list)
        if len(list) <=4:
            return None
        return list[4]

    # return the final status based on the email template and student repsponse
    def get_final_status(self):
        status = self.default_status

        r = self.get_response()
        if r is None:
            return status
        elif r == 'Leave':
            return 'Dismiss'
        elif r == 'Stay':
            return status
