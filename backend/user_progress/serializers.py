from rest_framework import serializers
from .models import UserProfile, LessonProgress


class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    name = serializers.CharField(source='user.first_name', read_only=True)
    level = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = [
            'email', 'name', 'points', 'streak', 'level',
            'lessons_completed', 'words_learned', 'exercises_done',
            'quiz_score', 'avatar_url', 'updated_at'
        ]

    def get_level(self, obj):
        return obj.get_level()


class LessonProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonProgress
        fields = ['lesson_id', 'lesson_title', 'completed', 'score', 'completed_at']
