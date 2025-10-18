from django.urls import path
from .views import OrganizationCreateView, OrganizationListView

app_name = 'organization'

urlpatterns = [
    path('create/', OrganizationCreateView.as_view(), name='organization-create'),
    path('list/', OrganizationListView.as_view(), name='organization-list'),
]
