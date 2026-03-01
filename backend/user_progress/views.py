from django.utils import timezone
from datetime import timedelta
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import UserProfile, LessonProgress
from .serializers import UserProfileSerializer, LessonProgressSerializer


def get_or_create_profile(user):
    profile, _ = UserProfile.objects.get_or_create(user=user)
    return profile


class ProfileStatsView(APIView):
    """Get full user stats & progression."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = get_or_create_profile(request.user)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)


class UpdateStatsView(APIView):
    """Patch user stats (points, streak, words, exercises, quiz_score)."""
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        profile = get_or_create_profile(request.user)
        fields = ['points', 'streak', 'words_learned', 'exercises_done', 'quiz_score']
        for field in fields:
            if field in request.data:
                setattr(profile, field, request.data[field])

        # Auto-level up
        profile.level = profile.get_level()
        profile.last_activity = timezone.now().date()
        profile.save()
        return Response(UserProfileSerializer(profile).data)


class AddPointsView(APIView):
    """Add points to the user (e.g after completing a lesson / exercise)."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        profile = get_or_create_profile(request.user)
        pts = request.data.get('points', 0)
        profile.points += int(pts)
        profile.level = profile.get_level()

        # Manage streak
        today = timezone.now().date()
        yesterday = today - timedelta(days=1)
        if profile.last_activity == yesterday:
            profile.streak += 1
        elif profile.last_activity != today:
            profile.streak = 1
        profile.last_activity = today
        profile.save()
        return Response({'points': profile.points, 'streak': profile.streak, 'level': profile.level})


class LessonCompleteView(APIView):
    """Mark a lesson as completed and record the score."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        lesson_id = request.data.get('lesson_id')
        lesson_title = request.data.get('lesson_title', '')
        score = request.data.get('score', 100.0)

        lesson_progress, created = LessonProgress.objects.update_or_create(
            user=request.user,
            lesson_id=lesson_id,
            defaults={
                'lesson_title': lesson_title,
                'completed': True,
                'score': score,
                'completed_at': timezone.now()
            }
        )

        # Update profile stats
        profile = get_or_create_profile(request.user)
        if created:
            profile.lessons_completed += 1
            profile.points += int(score)
            profile.level = profile.get_level()
            profile.save()

        return Response(LessonProgressSerializer(lesson_progress).data, status=status.HTTP_200_OK)


class LessonProgressListView(APIView):
    """List all lesson completions for the authenticated user."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        progress = LessonProgress.objects.filter(user=request.user)
        return Response(LessonProgressSerializer(progress, many=True).data)
