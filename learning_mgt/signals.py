from authentication.models import User
from learning_mgt.models import Student, EducationDetails, Mentor, MentorStudent, Performance
from django.dispatch import receiver
from django.db.models.signals import post_save
from authentication.utils import Util

@receiver(post_save, sender=User)
def create_student_details(sender, instance, created, **kwargs):
    """ receiver function that will create profile for an user instance
        Args:
            sender ([model class]): [user model class]
            instance ([model object]): [user model instance that is actually being saved]
            created ([boolean]): [true if new record has created in user model]
    """
    if created:
        if instance.role == 'Student':
            student = Student.objects.create(student=instance)
            EducationDetails.objects.create(student=student)
        elif instance.role == 'Mentor':
            Mentor.objects.create(mentor=instance)

@receiver(post_save, sender=MentorStudent)
def create_performance_instance(sender, instance, created, **kwargs):
    if created:
        Performance.objects.create(student=instance.student, course=instance.course, mentor=instance.mentor)

@receiver(post_save, sender=Performance)
def send_performance_email(sender, instance, created, **kwargs):
    if not created:
        data = {
            'email' : instance.student,
            'message' :  "Hii "+instance.student.get_full_name()+'\n'+'Your score for this week : \n'+"\nScore - "+str(instance.current_score),
            'subject' : 'Performance Report',
        }
        email = Util.email_data_generic(data)
        Util.send_email(email)