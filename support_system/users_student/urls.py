from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path('register/', views.register_student, name='register_student'),
                  path('username_avaliable/', views.username_avaliable, name='username_avaliable'),
                  path('login/', views.login_student, name='login_student'),
                  path('profile/', views.student_profile, name='student_profile'),
                  path('update_profile/', views.update_profile, name='update_profile'),
                  path('username_available_login/',views.username_available_login,name='username_available_login')

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
