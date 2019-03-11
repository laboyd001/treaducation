from django.db import models
from django.contrib.auth.models import User



class Subject(models.Model):
    '''the blueprints for a subject
    '''
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

class Course(models.Model):
    '''the blueprints for a course
    '''

    # instructor that created the course
    owner = models.ForeignKey(User,
                              related_name='courses_created',
                              on_delete=models.CASCADE)
    # subject that the course belong to
    subject = models.ForeignKey(Subject,
                              related_name='courses',
                              on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    # used in URLS
    slug = models.SlugField(max_length=200, unique=True)
    # overview of the course
    overview = models.TextField()
    # date and time when course was created
    created = models.DateTimeField(auto_now_add=True)
    # users that are enrolled in a course
    student = models.ManyToManyField(User, through='CourseStudent')

    class Meta:
        ordering = ['created']

    def __str__(self):
        return self.title

class Module(models.Model):
    '''the blueprints for a module
    '''
    course = models.ForeignKey(Course,
                              on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    text = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to = 'images/', default = 'images/no-img.jpg')

    def __str__(self):
        return self.title

class CourseStudent(models.Model):
    '''the blueprints for a student_course relationship
    '''

    course = models.ForeignKey(Course,
                            on_delete=models.CASCADE)
    student = models.ForeignKey(User,
                            on_delete=models.CASCADE)







