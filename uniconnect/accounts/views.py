from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.urls import reverse
from accounts.forms import SignUpForm, EditProfileForm, EditInterestsForm
from django.forms import modelformset_factory
from accounts.models import Interest, Profile, Tutorship
from django.db.models.functions import Concat
from django.db.models import Value, Count, Case, When, Q
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.template.context_processors import media
from courses.views import scrapeCourse
from courses.models import Courses

@login_required
def dashboard(request):
	followers = Profile.objects.filter(following=request.user.profile)
	return render(request, 'profile/info.html', {'current_user':request.user, 'followers':followers})


def signup(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=raw_password)
			if user is not None:
				login(request, user)
				return redirect('/dashboard')
	else:
		form = SignUpForm()
	return render(request, 'registration/signup.html', {'form': form})

@login_required
def editProfile(request):
	while len(request.user.interests.all()) < 3:
		i = Interest(user_id=request.user.id,interest='')
		i.save()
	
	interests = list(request.user.interests.all())
	interestsFormSet = modelformset_factory(Interest, form=EditInterestsForm, extra=0, fields=('user_id','interest'))
	if request.method == 'POST':
		profileForm = EditProfileForm(request.POST, request.FILES, instance=request.user.profile)
		interestsForms = interestsFormSet(request.POST, initial=interests[:3])
		if profileForm.is_valid() and interestsForms.is_valid():
			profileForm.save()
			interestsForms.save()
			return redirect('/dashboard')
	else:
		profileForm = EditProfileForm(instance=request.user.profile)
		interestsForms = interestsFormSet(initial=interests[:3], queryset=request.user.interests.all())
	return render(request, 'profile/edit.html', {'profileForm': profileForm, 'interestsForms':interestsForms})
	

def user(request, id=0):
	u = User.objects.get(id = id)
	followers = Profile.objects.filter(following=u.profile)
	return render(request, 'profile/info.html', {'current_user':u, 'followers':followers})
	
@login_required
def follow(request, id=0):
	u = User.objects.get(id = id)
	if u.profile in request.user.profile.following.all():
		request.user.profile.following.remove(u.profile)
	else:
		request.user.profile.following.add(u.profile)
	request.user.save()
	return JsonResponse({"following": (u.profile in request.user.profile.following.all())})
	
	
def search(request):
	users = []
	name = request.GET.get('name', '').strip()
	interest = request.GET.get('interest', '').strip()
	tutor = request.GET.get('tutor', False)
	sameCourses = request.GET.get('sameCourses', False)
	facebookFriends = request.GET.get('facebookFriends', False)
	if name or interest or tutor or sameCourses or facebookFriends:
		users = User.objects.all().exclude(id=request.user.id)
		if name:		users = users.annotate(fullname=Concat('first_name', Value(' '), 'last_name')).filter(fullname__icontains=name)
		if interest:	users = users.annotate(interestCount=Count('interests')).filter(interests__interest__icontains=interest, interestCount__gt=0)
		if tutor:		users = list(filter(lambda u: (Tutorship.objects.filter(user=u.profile, course__in=request.user.profile.currentCourses.all(), tutor=True).all()),users))
		for u in users:
			u.mutualCourses = u.profile.currentCourses.all()&(request.user.profile.currentCourses.all()) if request.user.is_authenticated else []
		if sameCourses:	users = filter(lambda u: u.mutualCourses,users)
		if facebookFriends:	users = filter(lambda u: u.profile.facebook and u.get_full_name() in [f['name'] for f in request.user.profile.facebook['friends']['data']],users)
		
		# Order results
		users = list(users)
		users.sort(key=lambda x:x.last_login, reverse=True)
		if request.user.is_authenticated:
			for u in users: 
				u.mutualInterests = set(map(str,u.interests.all()))&set(map(str,request.user.interests.all()))
			users.sort(key=lambda u:len(u.mutualCourses), reverse=True)
			users.sort(key=lambda u:len(u.mutualInterests), reverse=True)
	return render(request, 'profile/search.html', {'users':users, "name":name, "interest":interest, "tutor":tutor, "sameCourses":sameCourses, "facebookFriends":facebookFriends})
	
@login_required
def editCourses(request):
	addCourse = request.GET.get('addCourse', '').strip()
	if addCourse:
		try:
			c = Courses.objects.get(name = addCourse)
		except Exception as e:
			print("Course doesn't exist in db: Attempting web-scrape")
			# if doesn't exists, try to scrape and save
			c = scrapeCourse(addCourse)
		if c:
			request.user.profile.currentCourses.add(c)
			request.user.profile.save()
	finishCourse = request.GET.get('finishCourse', '').strip()
	if finishCourse:
		c = Courses.objects.get(name = finishCourse)
		request.user.profile.currentCourses.remove(c)
		request.user.profile.previousCourses.add(c)
		
	saveTutors = request.GET.get('saveTutors', '').strip()
	if saveTutors:
		for t in Tutorship.objects.filter(user=request.user.profile):
			t.tutor = bool(request.GET.get(t.course.name, False))
			t.save()
	tutorships = Tutorship.objects.filter(user=request.user.profile)
	return render(request, 'profile/editCourses.html', {"addCourse":addCourse, "tutorships":tutorships})