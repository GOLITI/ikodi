from django.urls import path
from .views import ProfileStatsView, UpdateStatsView, AddPointsView, LessonCompleteView, LessonProgressListView

urlpatterns = [
    path('stats/', ProfileStatsView.as_view(), name='profile_stats'),
    path('stats/update/', UpdateStatsView.as_view(), name='update_stats'),
    path('stats/add-points/', AddPointsView.as_view(), name='add_points'),
    path('lessons/', LessonProgressListView.as_view(), name='lesson_list'),
    path('lessons/complete/', LessonCompleteView.as_view(), name='lesson_complete'),
]
