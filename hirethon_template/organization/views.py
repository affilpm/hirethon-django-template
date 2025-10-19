from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Organization
from .serializers import OrganizationSerializer, OrganizationListSerializer, NamespaceSerializer
from .models import Membership, Role, Namespace

class OrganizationCreateView(generics.CreateAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        organization = serializer.save(created_by=self.request.user)

        Membership.objects.create(
            user=self.request.user,
            organization=organization,
            role=Role.ADMIN
        )
        


class OrganizationListView(generics.ListAPIView):
    serializer_class = OrganizationListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Return organizations where the user is a member or creator."""
        return Organization.objects.filter(memberships__user=self.request.user).distinct()

    def get_serializer_context(self):
        """Pass request to serializer to access the current user."""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context 
    

class NamespaceCreateView(generics.CreateAPIView):
    queryset = Namespace.objects.all()
    serializer_class = NamespaceSerializer
    permission_classes = [permissions.IsAuthenticated]    
    

class NamespaceListView(generics.ListAPIView):
    queryset = Namespace.objects.all()
    serializer_class = NamespaceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        org_id = self.request.query_params.get('organization')
        queryset = super().get_queryset()
        if org_id:
            queryset = queryset.filter(organization_id=org_id)
        return queryset    