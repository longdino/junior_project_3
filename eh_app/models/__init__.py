# TODO: Field validation

# FIXME: There needs to be a mandatory list of activities and advising that is required,
# and a list of tracked student participation elsewhere
# in track requirements and student status

from ._baseTimestampModel import _BaseTimestampModel

from .activity import Activity
from .activityAdvisingException import ActivityAdvisingException
from .advisor import Advisor
from .campus import Campus
from .college import College
from .course import Course
from .department import Department
from .emailTemplate import EmailTemplate
from .exception import Exception
from .gpaAndPartStatus import GPAAndPartStatus
from .gpaDeficiency import GPADeficiency
from .gpaStatus import GPAStatus
from .honorsCreditHoursRating import HonorsCreditHoursRating
from .major import Major
from .participationStatus import ParticipationStatus
from .probAndGpaDef import ProbAndGPADef
from .probDefStatus import ProbDefStatus
from .requirement import Requirement
from .research import Research
from .section import Section
from .semester import Semester
from .student import Student
from .studentAdvisorMeeting import StudentAdvisorMeeting
from .studentException import StudentException
from .studentResearch import StudentResearch
from .studentSectionEnrollment import StudentSectionEnrollment
from .studentSemesterStatus import StudentSemesterStatus
from .studentTrackEnrollment import StudentTrackEnrollment
from .teacher import Teacher
from .track import Track
from .trackRequirements import TrackRequirements
