from django.contrib import admin
from django.urls import path
from learning_mgt.views import UpdateStudentDetails, EducationDetailsList, Courses, CourseDetails, Mentors, MentorCourseMapping, MentorStudentMapping, MentorStudentDetails, PerformanceAPI, PerformanceDetailsAPI, UpdateEducationDetailsByCourse

urlpatterns = [
    path('student-details/<int:student_id>', UpdateStudentDetails.as_view(), name='student-details'),
    path('edu-details-list/<int:student_id>', EducationDetailsList.as_view(), name='edu-details-list'),
    path('edu-details/<int:id>', UpdateEducationDetailsByCourse.as_view(), name='edu-details'),
    path('courses/', Courses.as_view(), name='courses'),
    path('course/<int:id>', CourseDetails.as_view(), name='course'),
    path('mentors/', Mentors.as_view(), name='mentors'),
    path('mentor-student/', MentorStudentMapping.as_view(), name='mentor-student'),
    path('mentor-course/<int:mentor_id>', MentorCourseMapping.as_view(), name='mentor-course'),
    path('mentor-student/<int:search_id>', MentorStudentDetails.as_view(), name='mentor-student-details'),
    path('performance/', PerformanceAPI.as_view(), name='performance'),
    path('performance/<int:id>', PerformanceDetailsAPI.as_view(), name='performance-details')
]
