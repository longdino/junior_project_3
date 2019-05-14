from django.dispatch import Signal

# Custom signals
semester_change = Signal(providing_args=['old_current_sem'])
