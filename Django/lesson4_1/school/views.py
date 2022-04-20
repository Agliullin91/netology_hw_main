from django.views.generic import ListView
from django.shortcuts import render

from .models import Student


def students_list(request):
    students = Student.objects.all().prefetch_related('teacher')
    template = 'school/students_list.html'
    context = {'object_list': students}

    return render(request, template, context)
