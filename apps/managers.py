import datetime

from django.db import models
from django.utils import timezone


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class UserManager(SoftDeleteManager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

    def active_users(self):
        return super().get_queryset().filter(status='active')

    def by_role(self, role):
        return super().get_queryset().filter(teammembership__role=role).distinct()

    def team_members(self, team):
        return super().get_queryset().filter(
            teammembership__team=team,
            teammembership__status='active',
        )

    def recently_joined(self, days=30):
        since = timezone.now() - datetime.timedelta(days=days)
        return super().get_queryset().filter(date_joined__gte=since)

    def inactive_users(self, days=90):
        since = timezone.now() - datetime.timedelta(days=days)
        return super().get_queryset().filter(
            date_joined__gte=since,
            status='inactive',
        )


class ProjectManager(SoftDeleteManager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

    def active_project(self):
        return super().get_queryset().filter(
            task__status='in_progress',
            status='active',
        ).distinct()

    def by_team(self, team):
        return super().get_queryset().filter(
            team=team,
        )

    def over_due(self):
        return super().get_queryset().filter(status='archived')

    def recent_active(self, days=7):
        since = timezone.now() - datetime.timedelta(days=days)
        return super().get_queryset().filter(
            task__updated_at__gte=since,
        )
