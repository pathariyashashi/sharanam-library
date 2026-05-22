from django.db import models
from django.utils import timezone


# =========================
# STUDENT MODEL
# =========================

class Student(models.Model):

    fullname = models.CharField(max_length=100)

    username = models.CharField(max_length=100)

    email = models.EmailField()

    mobile = models.CharField(max_length=15)

    password = models.CharField(max_length=100)

    gender = models.CharField(max_length=20)

    dob = models.DateField()

    current_address = models.TextField()

    permanent_address = models.TextField()

    def __str__(self):

        return self.fullname


# =========================
# SEAT BOOKING MODEL
# =========================

class SeatBooking(models.Model):

    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    seat_number = models.CharField(max_length=10)

    time_slot = models.CharField(max_length=50)

    booking_date = models.DateField(auto_now_add=True)

    expiry_date = models.DateField(default=timezone.now)

    status = models.CharField(max_length=20, default="Active")

    floor = models.CharField(max_length=20, default="1st Floor")

    def __str__(self):

        return f"{self.student.fullname} - {self.seat_number}"


# =========================
# ATTENDANCE MODEL
# =========================

class Attendance(models.Model):

    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    date = models.DateField(auto_now_add=True)

    check_in = models.TimeField(null=True, blank=True)

    check_out = models.TimeField(null=True, blank=True)

    def __str__(self):

        return self.student.fullname


# =========================
# PAYMENT MODEL
# =========================

class Payment(models.Model):

    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    amount = models.IntegerField()

    payment_method = models.CharField(max_length=50)

    transaction_id = models.CharField(max_length=100)

    status = models.CharField(max_length=20, default="Pending")

    payment_date = models.DateField(auto_now_add=True)

    expiry_date = models.DateField(default=timezone.now)

    def __str__(self):

        return f"{self.student.fullname} - {self.status}"


# =========================
# NOTIFICATION MODEL
# =========================

class Notification(models.Model):

    title = models.CharField(max_length=200)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return self.title