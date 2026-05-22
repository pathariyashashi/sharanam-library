from django.contrib import admin

from .models import *
from .models import Attendance

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):

    list_display = (

        'student',

        'date',

        'check_in',

        'check_out'

    )

admin.site.register(SeatBooking)

admin.site.register(Payment)

admin.site.register(Notification)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):

    list_display = (
        'fullname',
        'username',
        'email',
        'mobile',
        'gender'
    )

    search_fields = (
        'fullname',
        'username',
        'email'
    )
    