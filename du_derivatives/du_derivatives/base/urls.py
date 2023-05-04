from django.contrib.auth import views as auth_views
from django.urls import path, include
from base.views import *

from base.forms import UserPasswordResetEmailForm

urlpatterns = [
    path('', home, name='home'),
    path('login', loginUser, name='login'),
    path('logout', logoutUser, name='logout'),
    path('signup', signup, name='signup'),
    path('activate-user/<str:uidb64>/<str:token>', activate_user, name='activate'),
    path('profile-<str:pk>', profile, name='profile'),
    path('userUpdate', userUpdate, name='userUpdate'),
    path('addProject', addProject, name='addProject'),
    path('addProjectCtd-<str:pk>', addProjectCtd, name='addProjectCtd'),
    path('projectUpdate-<str:pk>', projectUpdate, name='projectUpdate'),
    path('deletePhoto-<str:pk>', deletePhoto, name='deletePhoto'),
    path('deleteCollaborator-<str:pk>-<str:collaborator>', deleteCollaborator, name='deleteCollaborator'),
    path('deleteTag-<str:pk>-<str:tag>', deleteTag, name='deleteTag'),

    path('reset_password', auth_views.PasswordResetView.as_view(template_name='password_reset.html', form_class=UserPasswordResetEmailForm), name='reset_password'),
    path('reset_password_sent', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_form.html'), name='password_reset_confirm'),
    path('reset_password_complete', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_done'
                                                                                               '.html'),
         name='password_reset_complete'),

    path('projectDetails-<str:pk>', projectDetails, name='projectDetails'),
    path('addReply:<str:projectPK>:<str:reviewPK>', addReply, name='addReply'),
    path('update_rating', update_rating, name='update_rating'),
]