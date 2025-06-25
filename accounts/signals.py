from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from django.conf import settings
from .models import CustomUser

@receiver(post_save, sender=CustomUser)
def assign_user_group(sender, instance, created, **kwargs):
    """
    Assign user to a group based on their role after creation.
    """
    if created:
        role_group_map = {
            "student": "Students",
            "staff": "Staff",
            "admin": "Admins",
        }

        role = instance.role
        group_name = role_group_map.get(role)

        if group_name:
            group, _ = Group.objects.get_or_create(name=group_name)
            instance.groups.add(group)
