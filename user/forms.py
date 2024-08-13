# myapp/forms.py

from django import forms
from .models import StudentMarks,StudentAttendance

class EmailForm(forms.Form):
    email = forms.EmailField()

class OTPForm(forms.Form):
    otp = forms.CharField(max_length=6)

class PasswordResetForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        

class StudentMarksForm(forms.ModelForm):
    physics = forms.CharField(initial=0,required=False)
    chemistry = forms.CharField(initial=0,required=False)
    class Meta:
        model = StudentMarks
        fields = ('physics', 'chemistry')   

class StudentAttendanceForm(forms.ModelForm):
    attendance_physics=forms.CharField(initial=0,required=False)
    attendance_chemistry=forms.CharField(initial=0,required=False)
    class Meta:
        model=StudentAttendance
        fields=('attendance_physics','attendance_chemistry')
