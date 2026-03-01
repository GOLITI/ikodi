from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    points = models.IntegerField(default=0)
    streak = models.IntegerField(default=0)  # consecutive days
    level = models.CharField(max_length=50, default='Débutant')
    lessons_completed = models.IntegerField(default=0)
    words_learned = models.IntegerField(default=0)
    exercises_done = models.IntegerField(default=0)
    quiz_score = models.FloatField(default=0.0)  # percentage
    last_activity = models.DateField(null=True, blank=True)
    avatar_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} - {self.points} pts"

    def get_level(self):
        if self.points < 500:
            return 'Débutant'
        elif self.points < 1500:
            return 'Aventurier'
        elif self.points < 3000:
            return 'Explorateur'
        elif self.points < 6000:
            return 'Expert'
        else:
            return 'Maître'


class LessonProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lesson_progress')
    lesson_id = models.CharField(max_length=50)
    lesson_title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    score = models.FloatField(default=0.0)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'lesson_id')
