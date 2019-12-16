from django.db import models
from django.contrib.auth.models import User

class Courses(models.Model):
	name = models.CharField(max_length=8, unique=True)
	title = models.CharField(max_length=50)
	uoc = models.IntegerField()
	prerequisites = models.CharField(max_length=300)
	offeringTerms = models.CharField(max_length=300)
	description = models.CharField(max_length=2000)
	
	def __str__(self):
		return self.name

class Review(models.Model):
	feedback = models.CharField(max_length=300)
	rating = models.IntegerField(default=0)
	#date = models.DateField(auto_now=True)
	user = models.ForeignKey(User, related_name="reviews", on_delete=models.CASCADE)
	course = models.ForeignKey("Courses", related_name="reviews", on_delete=models.CASCADE)
	anonymous = models.BooleanField(default=False)