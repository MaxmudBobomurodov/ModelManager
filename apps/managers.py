import datetime

from django.db import models
from django.utils import timezone


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class UserManager(SoftDeleteManager):


    def active_users(self):
        return self.get_queryset().filter(status='active')

    def by_role(self, role):
        return self.get_queryset().filter(teammembership__role=role).distinct()

    def team_members(self, team):
        return self.get_queryset().filter(
            teammembership__team=team,
            teammembership__status='active',
        )

    def recently_joined(self, days=30):
        since = timezone.now() - datetime.timedelta(days=days)
        return self.get_queryset().filter(date_joined__gte=since)

    def inactive_users(self, days=90):
        since = timezone.now() - datetime.timedelta(days=days)
        return self.get_queryset().filter(
            date_joined__gte=since,
            status='inactive',
        )


class ProjectManager(SoftDeleteManager):


    def active_project(self):
        return self.get_queryset().filter(
            task__status='in_progress',
            status='active',
        ).distinct()

    def by_team(self, team):
        return self.get_queryset().filter(
            team=team,
        )

    def over_due(self):
        return self.get_queryset().filter(status='archived')

    def recent_active(self, days=7):
        since = timezone.now() - datetime.timedelta(days=days)
        return self.get_queryset().filter(
            task__updated_at__gte=since,
        )


class TaskManager(SoftDeleteManager):

    def pending_tasks(self):
        return self.get_queryset().exclude(
            status="done",
        )

    def by_assignee(self, user):
        return self.get_queryset().filter(
            assignee=user,
        )

    def by_priority(self, priority):
        return self.get_queryset().filter(
            priority=priority,
        )

    def over_due_tasks(self):
        return self.get_queryset().filter(
            due_date__lte=timezone.now(),
            status=['in_progress', 'todo'],
        )

    def team_tasks(self, user):
        return self.get_queryset().filter(
            project__team=user,
        )