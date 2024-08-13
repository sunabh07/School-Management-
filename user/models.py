from django.db import models

# Create your models here.
class teacher_info(models.Model):
    name=models.CharField(max_length=122)
    email=models.CharField(max_length=122)
    phone=models.CharField( max_length=12)
    address=models.CharField(max_length=122)
    aadhaar_no=models.CharField(max_length=12)
    teacher_id=models.CharField(max_length=100,primary_key=True)
    password = models.CharField(max_length=255,default='default_password')

    def __str__(self):
        return self.name

class student_info(models.Model):
    name=models.CharField(max_length=122)
    email=models.CharField(max_length=122)
    phone=models.CharField( max_length=12)
    address=models.CharField(max_length=122)
    aadhaar_no=models.CharField(max_length=12)
    class_of_stud=models.CharField(max_length=20)
    student_id=models.CharField(max_length=100,primary_key=True)
    password = models.CharField(max_length=255,default='default_password')
    
    def __str__(self):
        return self.name

class teacher_class_mapp(models.Model):
    teacher=models.ForeignKey(teacher_info,on_delete=models.CASCADE)    
    class_stud=models.CharField(max_length=20)
    def __str__(self):
        return f"{self.class_of_stud} taught by {self.teacher.name}"


class teacher_sub_mapp(models.Model):
    teacher=models.ForeignKey(teacher_info,on_delete=models.CASCADE)
    subject=models.CharField(max_length=20) 

    def  __str__(self):
        return f"{self.subject} taught by {self.teacher.name}" 
    

class StudentMarks(models.Model):
    student=models.ForeignKey(student_info,on_delete=models.CASCADE)
    physics=models.CharField(max_length=200,blank=True, null=True)
    chemistry=models.CharField(max_length=200,blank=True, null=True)

    def __str__(self):
        return  f"marks {self.chemistry} and {self.physics} of {self.student.name}"
    
class StudentAttendance(models.Model):
    student=models.ForeignKey(student_info,on_delete=models.CASCADE)
    attendance_physics=models.CharField(max_length=200,blank=True, null=True)
    attendance_chemistry=models.CharField(max_length=200,blank=True, null=True)

    def __str__(self):
        return f"Attendance in {self.attendance_physics} and {self.attendance_chemistry} of {self.student.name}"


class contactus(models.Model):
    name=models.CharField(max_length=20)
    email=models.CharField(max_length=122)
    subject=models.CharField(max_length=122)
    message=models.CharField(max_length=122)

    def __str__(self) -> str:
        return self.name

class paymenttable(models.Model):
    student=models.ForeignKey(student_info,on_delete=models.CASCADE)
    payment=models.BooleanField(default=False)

    def __str__(self):
        return self.student.name
    