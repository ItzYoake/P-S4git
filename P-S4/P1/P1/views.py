from django.shortcuts import render, redirect
from collections import defaultdict
from django.db.models import Count
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from Attendance.models import Attendance
from django.core.serializers import serialize
from datetime import datetime, timedelta
from django.contrib.auth import login, logout, authenticate
from Teacher.models import Teacher
from Student.models import Student
from django.db.models.functions import TruncMonth
from collections import defaultdict


def dashboard(request):
    # Retrieve all teachers and students
    myteachers = Teacher.objects.all()
    mystudents = Student.objects.all()
    
    # Calculate the counts of men and women among teachers
    teacher_gender_counts = myteachers.values('gender').annotate(count=Count('gender'))
    teacher_gender_dict = {entry['gender']: entry['count'] for entry in teacher_gender_counts}

    # Calculate the counts of men and women among students
    student_gender_counts = mystudents.values('gender').annotate(count=Count('gender'))
    student_gender_dict = {entry['gender']: entry['count'] for entry in student_gender_counts}

    # Ensure keys exist for both genders in the dictionaries
    teacher_gender_dict.setdefault('Male', 0)
    teacher_gender_dict.setdefault('Female', 0)
    student_gender_dict.setdefault('Male', 0)
    student_gender_dict.setdefault('Female', 0)

    # Prepare context with all data
    context = {
        'total_teachers': myteachers.count(),  # Total number of teachers
        'total_students': mystudents.count(),  # Total number of students
        'teacher_gender_counts': teacher_gender_dict,  # Gender counts for teachers
        'student_gender_counts': student_gender_dict,  # Gender counts for students
    }

    return render(request, 'dashboard.html', context)


# def dashboard(request):
#     form = {
#         "title": "My Dashboard",
#         "content": "MY CONTENT"
#     }
#     return render(request, "dashboard.html", {'form': form})


def permission_denied(request):
    if request.method == "POST":
        if 'next' in request.POST:
            path = str(request.POST.get('next')).split('/')[1]
            return redirect(f"/{path}")
            # return HttpResponse(f"/{path}")
    else:
        form = {
            "title": "Permission Denied",
            "content": "You dont have permission, Please contact the admin to continue with this action",
        }
        return render(request, "permission_denied.html", {'form': form})
