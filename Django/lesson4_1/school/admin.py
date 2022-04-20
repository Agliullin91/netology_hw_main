from django.contrib import admin

from .models import Student, Teacher


class TeachersInline(admin.TabularInline):
    model = Student.teacher.through
    extra = 0


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'group']
    inlines = [TeachersInline,]


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'subject']
