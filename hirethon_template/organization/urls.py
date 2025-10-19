from django.urls import path
from .views import OrganizationCreateView, OrganizationListView, NamespaceCreateView, NamespaceListView

app_name = 'organization'

urlpatterns = [
    path('create/', OrganizationCreateView.as_view(), name='organization_create'),
    path('list/', OrganizationListView.as_view(), name='organization_list'),
    path('namespace/', NamespaceListView.as_view(), name='namespace_list'),       
    path('namespace/create/', NamespaceCreateView.as_view(), name='namespace_create')
]
