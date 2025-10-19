from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Organization, Membership, Role

@receiver(post_save, sender=User)
def create_organization_for_user(sender, instance, created, **kwargs):
    if created:
        # Create an organization for the new user
        organization = Organization.objects.create(
            name=f"{instance.name or instance.email}'s Organization",
            created_by=instance
        )

        # Create Membership as Admin for the creator
        Membership.objects.create(
            user=instance,
            organization=organization,
            role=Role.ADMIN
        )