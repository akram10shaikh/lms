from course.models import Enrollment

def is_user_enrolled(user, course):
    return Enrollment.objects.filter(user=user, course=course).exists()