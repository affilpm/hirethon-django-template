from rest_framework import serializers
from .models import Organization, Namespace

class OrganizationSerializer(serializers.ModelSerializer):
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
    


