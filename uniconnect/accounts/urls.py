from django.contrib.auth import views as auth_views
from django.urls import path, re_path
from accounts.forms import CustomAuthForm
from accounts import views as accounts_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
	path('dashboard/', accounts_views.dashboard, name='dashboard'),
	path('login/', auth_views.LoginView.as_view(template_name='registration/login.html', authentication_form=CustomAuthForm), name='login'),
	path('logout/', auth_views.LogoutView.as_view(template_name='registration/logged_out.html'), name='logout'),
	path('signup/', accounts_views.signup, name='signup'),
	path('editProfile/', accounts_views.editProfile, name='editProfile'),
	path('user/<int:id>', accounts_views.user, name='user'),
	path('follow/<int:id>', accounts_views.follow, name='follow'),
	path('search/', accounts_views.search, name='user_search'),
	path('editCourses/', accounts_views.editCourses, name='editCourses'),
] +  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)