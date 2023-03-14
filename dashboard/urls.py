from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_dashboard, name='dashboard'),
    path('delete/<int:id>', views.delete_user, name='delete'),
    path('edit-user/<int:id>', views.edit_user, name='edit'),
    path('update/<int:id>', views.update_user, name='update'),
    path('new-user', views.create_user, name='create'),
]
