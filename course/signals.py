from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from .models import Review

@receiver(post_save,sender=Review)
def update_course_rating_on_save(sender,instance,**kwargs):
    instance.course.update_rating_stats()

@receiver(post_delete,sender=Review)
def update_course_rating_on_delete(sender,instance,**kwargs):
    instance.course.update_rating_stats()