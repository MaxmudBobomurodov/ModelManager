from django.apps import AppConfig

from page.models import BookModel


class LibraryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'library'

    def ready(self):
        from django.contrib.auth.models import Group, Permission
        from django.contrib.contenttypes.models import ContentType
        from django.db.models.signals import post_migrate

        def create_roles(sender, **kwargs):
            content_type = ContentType.objects.get_for_model(BookModel)


            roles = {
                "Reader":["view_book"],
                "Librarian":["view_book", "add_book", "change_book"],
                "Admin": ["view_book", "add_book", "change_book", "delete_book"],

            }

            for role_name, perms in roles.items():
                group, created = Group.objects.get_or_create(name=role_name)
                for perm in perms:
                    permission = Permission.objects.get(codename=perm, content_type=content_type)
                    group.permissions.add(permission)

            post_migrate.connect(create_roles, sender=self)