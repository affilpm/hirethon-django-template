from rest_framework import serializers
from .models import Organization, Namespace
from rest_framework.validators import UniqueValidator

class OrganizationSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        max_length=100,
        validators=[
            UniqueValidator(
                queryset=Organization.objects.all(),
                message="An organization with this name already exists."
            )
        ]
    )

    class Meta:
        model = Organization
        fields = ['id', 'name', 'created_by', 'created_at']
        read_only_fields = ['id', 'created_by', 'created_at']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['created_by'] = user
        return super().create(validated_data)

class OrganizationListSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()
    member_count = serializers.SerializerMethodField()

    class Meta:
        model = Organization
        fields = ['id', 'name', 'role', 'member_count', 'created_at']

    def get_role(self, obj):
        """Return the current user's role in this organization."""
        user = self.context['request'].user
        membership = obj.memberships.filter(user=user).first()
        return membership.role if membership else None

    def get_member_count(self, obj):
        """Return the number of members in this organization."""
        return obj.memberships.count()    
    


class NamespaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Namespace
        fields = ['id', 'name', 'organization', 'created_by', 'created_at']
        read_only_fields = ['id', 'created_by', 'created_at']

    def validate_organization(self, value):
        user = self.context['request'].user
        # Check if the user is admin in the organization
        if not value.memberships.filter(user=user, role='admin').exists():
            raise serializers.ValidationError("You are not an admin of this organization")
        return value

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)