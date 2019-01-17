from django import forms

from .models import Employee

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'employment_position', 'employment_start_date', 'salary', 'employment_photo', 'parent']