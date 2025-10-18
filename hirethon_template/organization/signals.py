from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Organization

@receiver(post_save, sender=User)
def create_organization_for_user(sender, instance, created, **kwargs):
    if created:
        # Create an organization for the new user
        Organization.objects.create(
            name=f"{instance.name or instance.email}'s Organization",
            created_by=instance
        )