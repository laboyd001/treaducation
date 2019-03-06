from django.contrib import admin
from .models import Subject, Course, Module



@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    '''This adds the subjects to the django admin portal
    '''

    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}


class ModuleInline(admin.StackedInline):
    model = Module


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    '''This adds the courses to the django admin portal
    '''

    list_display = ['title', 'subject', 'created']
    list_filter = ['created', 'subject']
    search_fields = ['title', 'overview']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ModuleInline]
