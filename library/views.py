from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .models import Student
from .models import Attendance
from datetime import datetime
from .models import Notification
from .models import *
from datetime import date, timedelta
import random
from django.http import HttpResponse

from reportlab.pdfgen import canvas
# Create your views here.
def home(request):
    return render(request, 'library/home.html')
# REGISTER
def register(request):

    if request.method == 'POST':

        fullname = request.POST['fullname']
        username = request.POST['username']
        email = request.POST['email']
        mobile = request.POST['mobile']
        dob = request.POST['dob']
        gender = request.POST['gender']
        current_address = request.POST['current_address']
        permanent_address = request.POST['permanent_address']
        password = request.POST['password']

        student = Student(

            fullname=fullname,
            username=username,
                        email=email,
            mobile=mobile,
            dob=dob,
            gender=gender,
            current_address=current_address,
            permanent_address=permanent_address,
            password=password

        )

        student.save()

        return redirect('login')

    return render(request, 'library/register.html')

# LOGIN
# LOGIN PAGE
def login_view(request):

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        try:

            student = Student.objects.get(
                username=username,
                password=password
            )

            request.session['student_id'] = student.id

            return redirect('dashboard')

        except:

            return render(request,
                          'library/login.html',
                          {'error':'Invalid Username or Password'})

    return render(request, 'library/login.html')
# DASHBOARD PAGE

def dashboard(request):

    student_id = request.session.get('student_id')

    if not student_id:

        return redirect('login')

    student = Student.objects.get(id=student_id)

    # =========================
    # ATTENDANCE ANALYTICS
    # =========================

    total_attendance = Attendance.objects.filter(

        student=student

    ).count()

    present_days = Attendance.objects.filter(

        student=student,

        check_in__isnull=False

    ).count()

    absent_days = total_attendance - present_days

    if total_attendance > 0:

        attendance_percentage = int(

            (present_days / total_attendance) * 100

        )

    else:

        attendance_percentage = 0

    # =========================
    # PAYMENT & BOOKING
    # =========================

    payment = Payment.objects.filter(

        student=student

    ).last()

    booking = SeatBooking.objects.filter(

        student=student

    ).last()

    # =========================
    # TODAY ATTENDANCE
    # =========================

    today = datetime.now().date()

    attendance = Attendance.objects.filter(

        student=student,

        date=today

    ).first()

    # =========================
    # NOTIFICATIONS
    # =========================

    notifications = Notification.objects.all().order_by('-id')

    # =========================
    # RENDER
    # =========================

    return render(

        request,

        'library/dashboard.html',

        {

            'student': student,

            'attendance': attendance,

            'notifications': notifications,

            'payment': payment,

            'booking': booking,

            'attendance_percentage': attendance_percentage,

            'present_days': present_days,

            'absent_days': absent_days,

        }

    )
def logout_view(request):

    request.session.flush()

    return redirect('login')
def logout_view(request):

    request.session.flush()

    return redirect('home')
def edit_profile(request):

    student_id = request.session.get('student_id')

    if not student_id:

        return redirect('login')

    student = Student.objects.get(id=student_id)

    if request.method == 'POST':

        student.fullname = request.POST['fullname']

        student.email = request.POST['email']

        student.mobile = request.POST['mobile']

        student.current_address = request.POST['current_address']

        student.permanent_address = request.POST['permanent_address']

        student.save()

        return redirect('dashboard')

    return render(
        request,
        'library/edit_profile.html',
        {'student':student}
    )
 
def mark_entry(request):

    student_id = request.session.get('student_id')

    if not student_id:
        return redirect('login')

    student = Student.objects.get(id=student_id)

    today = datetime.now().date()

    attendance, created = Attendance.objects.get_or_create(
        student=student,
        date=today
    )

    attendance.check_in = datetime.now().time()

    attendance.save()

    return redirect('dashboard')   

def mark_exit(request):

    student_id = request.session.get('student_id')

    if not student_id:
        return redirect('login')

    student = Student.objects.get(id=student_id)

    today = datetime.now().date()

    attendance = Attendance.objects.get(
        student=student,
        date=today
    )

    attendance.check_out = datetime.now().time()

    attendance.save()

    return redirect('dashboard')
def gallery(request):

    return render(request,'library/gallery.html')
def about(request):

    return render(request,'library/about.html')
def address(request):

    return render(request,'library/address.html')
def updates(request):

    notifications = Notification.objects.all().order_by('-id')

    return render(
        request,
        'library/updates.html',
        {
            'notifications': notifications
        }
    )
def rules(request):

    return render(request,'library/rules.html')

def attendance_history(request):

    student_id = request.session.get('student_id')

    if not student_id:
        return redirect('login')

    student = Student.objects.get(id=student_id)

    records = Attendance.objects.filter(student=student).order_by('-date')

    return render(request,
        'library/attendance_history.html',
        {
            'records': records
        }
    )
def seat_booking(request):

    student_id = request.session.get("student_id")

    if not student_id:

        return redirect("login")

    booked_seats = SeatBooking.objects.values_list(

        'seat_number',

        flat=True

    )

    available_seats = [

        "A-1","A-2","A-3","A-4",

        "B-1","B-2","B-3","B-4"

    ]

    available_seats = [

        seat for seat in available_seats

        if seat not in booked_seats

    ]

    if request.method == "POST":

        seat = request.POST.get("seat")

        slot = request.POST.get("slot")

        return redirect(

            f"/payment/?seat={seat}&slot={slot}"

        )

    return render(

        request,

        "library/seat_booking.html",

        {

            'available_seats': available_seats

        }

    )

# =========================
# PAYMENT PAGE
# =========================

def payment(request):

    student_id = request.session.get("student_id")

    if not student_id:

        return redirect("login")

    student = Student.objects.get(id=student_id)

    seat = request.GET.get("seat")

    slot = request.GET.get("slot")

    if request.method == "POST":

        transaction_id = "TXN" + str(random.randint(10000,99999))

        expiry = timezone.now().date() + timedelta(days=30)

        Payment.objects.create(

            student=student,

            amount=1500,

            payment_method="UPI",

            transaction_id=transaction_id,

            status="Paid",

            expiry_date=expiry

        )

        SeatBooking.objects.create(

            student=student,

            seat_number=seat,

            time_slot=slot

        )

        return redirect("dashboard")

    return render(

        request,

        "library/payment.html",

        {

            "seat": seat,

            "slot": slot

        }

    )

# =========================
# PAYMENT SUCCESS
# =========================
def payment_success(request):

    student_id = request.session.get("student_id")

    student = Student.objects.get(id=student_id)

    seat = request.GET.get("seat")

    transaction = "TXN" + str(random.randint(100000,999999))

    expiry = date.today() + timedelta(days=30)

    Payment.objects.create(

        student=student,

        amount=1500,

        payment_method="UPI",

        transaction_id=transaction,

        status="Paid",

        expiry_date=expiry

    )

    SeatBooking.objects.create(

        student=student,

        seat_number=seat,

        status="Active",

        expiry_date=expiry

    )

    return redirect("dashboard")

def download_receipt(request):

    student_id = request.session.get("student_id")

    student = Student.objects.get(id=student_id)

    payment = Payment.objects.filter(student=student).last()

    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = 'attachment; filename="receipt.pdf"'

    pdf = canvas.Canvas(response)

    pdf.setFont("Helvetica-Bold", 18)

    pdf.drawString(180, 800, "Library Payment Receipt")

    pdf.setFont("Helvetica", 14)

    pdf.drawString(100, 740, f"Student Name : {student.fullname}")

    pdf.drawString(100, 700, f"Amount Paid : ₹{payment.amount}")

    pdf.drawString(100, 660, f"Payment Status : {payment.status}")

    pdf.drawString(100, 620, f"Transaction ID : {payment.transaction_id}")

    pdf.drawString(100, 580, f"Expiry Date : {payment.expiry_date}")

    pdf.drawString(100, 500, "Thank You For Joining Sharanam Library")

    pdf.save()

    return response