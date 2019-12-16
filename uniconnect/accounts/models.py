from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from social_django.fields import JSONField
from courses.models import Courses

def user_profile_path(profile, filename):
	return "user_"+str(profile.user.id)+"/profile.jpg"

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	
	degree = models.CharField(max_length=50)
	biography = models.CharField(max_length=300)
	image = models.ImageField(default='default/myprofile.jpg', upload_to=user_profile_path)
	
	facebook = JSONField()
	
	following = models.ManyToManyField("self", symmetrical=False)
	currentCourses = models.ManyToManyField(Courses, related_name='currentCourses')
	previousCourses = models.ManyToManyField(Courses, through="Tutorship", related_name='previousCourses')
	
	def __str__(self):
		return self.name

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	instance.profile.save()

class Interest(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='interests')
	interest = models.CharField(max_length=30)
	
	def __str__(self):
		return self.interest
		
		
class Tutorship(models.Model):
	user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="tutors")
	course = models.ForeignKey(Courses, on_delete=models.CASCADE)
	tutor = models.BooleanField(default=False)