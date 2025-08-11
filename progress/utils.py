from progress.models import SyllabusProgress
from content.models import Syllabus

def calculate_course_progress_percent(user, course):
    total_syllabus = Syllabus.objects.filter(course=course).count()
    if total_syllabus == 0:
        return 0.0

    completed = SyllabusProgress.objects.filter(
        student = user,
        syllabus__course = course,
        is_completed = True
    ).count()
    return round((completed/total_syllabus)*100,2)