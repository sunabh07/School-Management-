from django.shortcuts import render, HttpResponse ,redirect,get_object_or_404
from .models import teacher_info, student_info, teacher_class_mapp,StudentMarks,StudentAttendance,teacher_sub_mapp,contactus,paymenttable
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail,EmailMessage
from .forms import EmailForm, OTPForm, PasswordResetForm,StudentMarksForm,StudentAttendanceForm
from .utils import generate_otp
from django.db import connection
from django.db.models import F, Avg
import razorpay
from django.conf import settings

# Create your views here.
def index(request):
    return render(request,'index.html')
def about(request):
    return render(request,'about.html')
def contact(request):
    if request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        subject=request.POST.get('subject')
        message=request.POST.get('message')
        Contact=contactus(name=name,email=email,subject=subject,message=message)
        Contact.save()
        messages.success(request, "Message has been sent.")
    return render(request,'contact.html')
def teacher(request):
    if request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        address=request.POST.get('address')                                                          
        aadhar_no=request.POST.get('aadhar_no')
        teacher_id=request.POST.get('teacher_id')
        password=request.POST.get('password')
        teacher=teacher_info(name=name,email=email,phone=phone,address=address,aadhaar_no=aadhar_no,teacher_id=teacher_id,password=password)
        teacher.save()
        messages.success(request, "Message has been sent.")
    return render(request,'teacher.html')
def student(request):
    if request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        address=request.POST.get('address')                                                          
        aadhar_no=request.POST.get('aadhar_no')
        class_of_stud=request.POST.get('class_of_stud')
        student_id=request.POST.get('student_id')
        password=request.POST.get('password')
        student=student_info(name=name,email=email,phone=phone,address=address,aadhaar_no=aadhar_no,class_of_stud=class_of_stud,student_id=student_id,password=password)
        student.save()
        messages.success(request, "Message has been sent.")
    return render(request,'student.html')



def loginteacher(request):
    if request.method=="POST":
        identifier=request.POST.get('name')
        password=request.POST.get('password')
        if identifier and password:
            # Check if the identifier is an email
            try:
                validate_email(identifier)
                teacher = teacher_info.objects.get(email=identifier, password=password)
                request.session['tname']=teacher.name
                request.session['tid']=teacher.teacher_id
                return redirect('teacher_dashboard')  # Redirect to the dashboard if the teacher exists
            except ValidationError:
                # If not an email, treat it as a phone number
                try:
                    teacher = teacher_info.objects.get(phone=identifier, password=password)
                    request.session['tname']=teacher.name
                    request.session['tid']=teacher.teacher_id
                    return redirect('teacher_dashboard')  # Redirect to the dashboard if the teacher exists
                except teacher_info.DoesNotExist:
                    messages.error(request, 'Invalid email/phone number or password')
                    
            except teacher_info.DoesNotExist:
                messages.error(request,'Invalid email/phone number or password')
        else:
            messages.error(request,'Invalid email/phone number or password')
        return render(request, 'login_teacher.html')
    return render(request, 'login_teacher.html')



def loginstudent(request):
    if request.method=="POST":
        identifier=request.POST.get('name')
        password=request.POST.get('password')
        if identifier and password:
            # Check if the identifier is an email
            try:
                validate_email(identifier)
                student = student_info.objects.get(email=identifier, password=password)
                request.session['sname']=student.name
                request.session['sid']=student.student_id
                request.session['sclass']=student.class_of_stud
                return redirect('student_dashboard')  # Redirect to the dashboard if the teacher exists
            except ValidationError:
                # If not an email, treat it as a phone number
                try:
                    student = student_info.objects.get(phone=identifier, password=password)
                    request.session['sname']=student.name
                    request.session['sid']=student.student_id
                    request.session['sclass']=student.class_of_stud
                    return redirect('student_dashboard')  # Redirect to the dashboard if the teacher exists
                except student_info.DoesNotExist:
                    messages.error(request, 'Invalid email/phone number or password')
                    
            except student_info.DoesNotExist:
                messages.error(request,'Invalid email/phone number or password')
        else:
            messages.error(request,'Invalid email/phone number or password')
        return render(request, 'login_student.html')
    return render(request, 'login_student.html')








def forgot_password(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            print(f"Email entered: {email}")  # Debugging print statement
            try:
                # Ensure case-insensitive comparison of email
                teacher = teacher_info.objects.get(email__iexact=email)
                print(f"Teacher found: {teacher.email}")  # Debugging print statement
                otp = generate_otp()
                request.session['otp'] = otp
                request.session['email'] = email
                send_mail(
                    'Your OTP Code',
                    f'Your OTP code is {otp}',
                    'sunabhmaheshwari07@gmail.com',
                    [email],
                    fail_silently=False,
                )
                return redirect('verify_otp')
            except teacher_info.DoesNotExist:
                print(f"Teacher with email {email} does not exist")  # Debugging print statement
                form.add_error('email', 'Email does not exist')
        else:
            print("Form is not valid")  # Debugging print statement
    else:
        form = EmailForm()
    return render(request, 'forgot_password.html', {'form': form})

def verify_otp(request):
    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data['otp']
            if otp == request.session.get('otp'):
                return redirect('reset_password')
            else:
                form.add_error('otp', 'Invalid OTP')
    else:
        form = OTPForm()
    return render(request, 'verify_otp.html', {'form': form})



def reset_password(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            email = request.session.get('email')
            if email:
                try:
                    teacher_info.objects.filter(email=email).update(password=new_password)
                    request.session.flush()
                    return redirect('password_reset_success')
                except teacher_info.DoesNotExist:
                    form.add_error(None, 'User does not exist')
    else:
        form = PasswordResetForm()
    return render(request, 'reset_password.html', {'form': form})






        

# @login_required
def teacher_dashboard(request):
    teacher_name=request.session.get('tname')
    teacher_id=request.session.get('tid')
    classes=teacher_class_mapp.objects.filter(teacher_id=teacher_id).values_list('class_stud',flat=True).distinct()
    return render(request,'teacher_dashboard.html',{'name':teacher_name,'classes':classes})

def mark1(request):
    teacher_name=request.session.get('tname')
    teacher_id=request.session.get('tid')
    classes=teacher_class_mapp.objects.filter(teacher_id=teacher_id).values_list('class_stud',flat=True).distinct()
    if request.method=='POST':
        class_id=request.POST.get('Classes')
        request.session['c']=class_id
        return redirect('mark2')
    return render(request,'mark1.html',{'name':teacher_name,'classes':classes})


def mark2(request):
    class_id=request.session.get('c')
    students = student_info.objects.filter(class_of_stud=class_id)
    forms=[]
    for student in students:
        student_marks, created = StudentMarks.objects.get_or_create(student=student)
        forms.append((student, StudentMarksForm(instance=student_marks, prefix=str(student.student_id))))
    if request.method == 'POST':
          for student, form in forms:
            form = StudentMarksForm(request.POST, prefix=str(student.student_id), instance=StudentMarks.objects.get(student=student))
            if form.is_valid():
                    student_marks.physics = form.cleaned_data.get('physics')
                    student_marks.chemistry = form.cleaned_data.get('chemistry')
                    student_marks.save()
                    send_mail(
                        'Regarding Marks',
                        f'hello {student_marks.student.name} your marks has been updated',
                        'sunabhmaheshwari07@gmail.com',
                        [student_marks.student.email],
                        fail_silently=False,

                    )


        # return redirect('mark2')
            
            return redirect('mark2')
    return render(request, 'mark2.html', {'forms': forms, 'class_id': class_id})
    

def attendance1(request):
    teacher_name=request.session.get('tname')
    teacher_id=request.session.get('tid')
    classes=teacher_class_mapp.objects.filter(teacher_id=teacher_id).values_list('class_stud',flat=True).distinct()
    if request.method=='POST':
        class_id=request.POST.get('Classes')
        request.session['c1']=class_id
        return redirect('attendance2')
    return render(request,'attendance1.html',{'name':teacher_name,'classes':classes})



def attendance2(request):
    class_id=request.session.get('c1')
    students = student_info.objects.filter(class_of_stud=class_id)
    forms=[]
    for student in students:
        student_attendance, created = StudentAttendance.objects.get_or_create(student=student)
        forms.append((student, StudentAttendanceForm(instance=student_attendance, prefix=str(student.student_id))))
    if request.method == 'POST':
          for student, form in forms:
            form = StudentAttendanceForm(request.POST, prefix=str(student.student_id), instance=StudentAttendance.objects.get(student=student))
            if form.is_valid():
                    student_attendance.attendance_physics = form.cleaned_data.get('attendance_physics')
                    student_attendance.attendance_chemistry = form.cleaned_data.get('attendance_chemistry')
                    student_attendance.save()
                    send_mail(
                        'Regarding Attendance',
                        f'hello {student_attendance.student.name} your attendance has been updated',
                        'sunabhmaheshwari07@gmail.com',
                        [student_attendance.student.email],
                        fail_silently=False,

                    )            
            return redirect('attendance2')
    return render(request,'attendance2.html',{'forms': forms, 'class_id': class_id})      



def notice1(request):
    teacher_name=request.session.get('tname')
    teacher_id=request.session.get('tid')
    classes=teacher_class_mapp.objects.filter(teacher_id=teacher_id).values_list('class_stud',flat=True).distinct()
    if request.method=='POST':
        class_id=request.POST.get('Classes')
        request.session['c']=class_id
        email_option = request.POST.get('email_option')
        if email_option == 'all':
            return redirect('notice_all')
        elif email_option == 'selected':
            return redirect('notice_selected')
    return render(request,'notice1.html',{'name':teacher_name,'classes':classes})


def notice_all(request):
    classs=request.session.get('c')
    if request.method == 'POST':
        
        message = request.POST.get('message')
        students = student_info.objects.filter(class_of_stud=classs)
        recipient_list = [student.email for student in students]
        to_email = recipient_list[0]
        cc_emails = recipient_list[1:]

        # Create an EmailMessage object
        email = EmailMessage(
            'New Notice has been Published',
            message,
            'sunabhmaheshwari07@gmail.com',
            [to_email],
            cc=cc_emails,
        )

        # Send the email
        email.send(fail_silently=False)
        messages.success(request, "Notice has been sent")

        
        # return redirect('success_url')  # Replace with your success URL

    return render(request, 'notice_all.html')


def notice_selected(request):
    classs=request.session.get('c')
    if request.method == 'POST':
        message = request.POST.get('message')
        selected_emails = request.POST.getlist('emails')
        to_email = selected_emails[0]
        cc_emails = selected_emails[1:]

        # Create an EmailMessage object
        email = EmailMessage(
            'New Notice has been Published',
            message,
            'sunabhmaheshwari07@gmail.com',
            [to_email],
            cc=cc_emails,
        )

        # Send the email
        email.send(fail_silently=False)
        messages.success(request, "Notice has been sent")

        

        # return redirect('success_url')  # Replace with your success URL

    students = student_info.objects.filter(class_of_stud=classs)
    return render(request, 'notice_selected.html', {'students': students})


def student_dashboard(request):
    sname=request.session.get('sname')
    
    return render(request,'student_dashboard.html',{'name':sname})

def student_marks(request):
    sname=request.session.get('sname')
    sid=request.session.get('sid')
    
    student_marks = get_object_or_404(StudentMarks, student_id=sid)
    if student_marks.physics is "":

        m_physics = "marks has not been updated"
        physics_status=""
    else:
        m_physics=student_marks.physics
        if student_marks.physics< '40':
            physics_status="FAIL"
        else:    
            physics_status ="PASS"
       

    if student_marks.chemistry is "":
        m_chemistry="marks has not been updated"
        chemistry_status=""
    else:
        m_chemistry=student_marks.chemistry
        if student_marks.chemistry <'40':
            chemistry_status="FAIL"
        else:
            chemistry_status="PASS"



    return render(request,'student_marks.html',{'name':sname,'m_physics':m_physics,'m_chemistry':m_chemistry,'chemistry_status':chemistry_status,'physics_status':physics_status})




        

def student_attendance(request):
    name = request.session.get('sname')
    id = request.session.get('sid')
    student_attendance = get_object_or_404(StudentAttendance, student=id)

    if student_attendance.attendance_physics == "":
        a_physics = "Attendance has not been updated"
        physics_status = ""
    else:
        a_physics = student_attendance.attendance_physics
        if int(a_physics) < 70:
            physics_status = "Low"
        else:
            physics_status = "Good"

    if student_attendance.attendance_chemistry == "":
        a_chemistry = "Attendance has not been updated"
        chemistry_status = ""
    else:
        a_chemistry = student_attendance.attendance_chemistry
        if int(a_chemistry) < 70:
            chemistry_status = "Low"
        else:
            chemistry_status = "Good"

    return render(request, 'student_attendance.html', {
        'name': name,
        'a_physics': a_physics,
        'physics_status': physics_status,
        'a_chemistry': a_chemistry,
        'chemistry_status': chemistry_status
    })
        


def subject_detail(request):
    Classes=request.session.get('sclass') 
    teacher_class_mappings = teacher_class_mapp.objects.filter(class_stud=Classes)
    
    
    # Prepare a list of teachers with their subjects
    teachers_info = []
    for mapping in teacher_class_mappings:
        teacher = mapping.teacher
        subjects = teacher_sub_mapp.objects.filter(
            teacher=teacher,
        ).values_list('subject', flat=True)
        print(f"Teacher: {teacher.name}, Subjects: {list(subjects)}")
        teachers_info.append({
            'name': teacher.name,
            'email': teacher.email,
            'subjects': ', '.join(subjects)  # Join subjects into a comma-separated string
        })
    
    return render(request, 'subject_detail.html', {'class': Classes, 'teachers_info': teachers_info})


def payment2(request):

    client=razorpay.Client(auth=(settings.KEY,settings.SECRET))
    payment=client.order.create({'amount':50000*100,'currency':'INR','payment_capture':1})


    return render(request,'payment2.html',{'order_id':payment['id']})





def forgot_passwordS(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            print(f"Email entered: {email}")  # Debugging print statement
            try:
                # Ensure case-insensitive comparison of email
                teacher = student_info.objects.get(email__iexact=email)
                print(f"Student found: {teacher.email}")  # Debugging print statement
                otp = generate_otp()
                request.session['otp'] = otp
                request.session['email'] = email
                send_mail(
                    'Your OTP Code',
                    f'Your OTP code is {otp}',
                    'sunabhmaheshwari07@gmail.com',
                    [email],
                    fail_silently=False,
                )
                return redirect('verify_otpS')
            except student_info.DoesNotExist:
                print(f"Student with email {email} does not exist")  # Debugging print statement
                form.add_error('email', 'Email does not exist')
        else:
            print("Form is not valid")  # Debugging print statement
    else:
        form = EmailForm()
    return render(request, 'forgot_passwordS.html', {'form': form})

def verify_otpS(request):
    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data['otp']
            if otp == request.session.get('otp'):
                return redirect('reset_passwordS')
            else:
                form.add_error('otp', 'Invalid OTP')
    else:
        form = OTPForm()
    return render(request, 'verify_otpS.html', {'form': form})



def reset_passwordS(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            email = request.session.get('email')
            if email:
                try:
                    student_info.objects.filter(email=email).update(password=new_password)
                    request.session.flush()
                    return redirect('password_reset_success')
                except student_info.DoesNotExist:
                    form.add_error(None, 'User does not exist')
    else:
        form = PasswordResetForm()
    return render(request, 'reset_passwordS.html', {'form': form})