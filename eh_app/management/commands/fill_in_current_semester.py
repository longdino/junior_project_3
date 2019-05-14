# TODO: This file should, with the proper arguments, call the parse commands for courses, activities, advising
# After calling the parsing commands, this command file should trigger the new_current(id=#) command to finalize the
# previous semester statuses. New current semester id and other info should be taken as arguments from CLI.
# NOTE: This command should attempt to restrict parsing data to just the current semester. This info can be found
# by calling Semester.objects.get_current(). Restriction may require adding params to each parsing command.
# FIXME: Parsing commands should maybe update semester status if information from previous semesters is changed.
# This could be prevented through removing all functionality of parsing except for the current semester (i.e., getting
# rid of the commands and just making them functions). 
