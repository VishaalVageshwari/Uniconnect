from django.shortcuts import render, reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from .models import Courses, Review
import re
from courses.forms import ReviewForm
# For web-scraping
import requests
from bs4 import BeautifulSoup

def info(request, name=""):
	if name:
		# try and select the course from the db
		try:
			c = Courses.objects.get(name = name)
		except Exception as e:
			print("Course doesn't exist in db: Attempting web-scrape")
			# if doesn't exists, try to scrape and save
			c = scrapeCourse(name)
		if c:
			c.description = addCourseURLS(c.description, [name])
			if c.prerequisites: c.prerequisites = addCourseURLS(c.prerequisites, [name])
			
			if request.method == 'POST':
				form = ReviewForm(request.POST, instance=Review(user=request.user,course=c, anonymous='anon' in request.POST))
				if form.is_valid():
					form.save()
					form = ReviewForm(instance=Review(course = c, user=request.user, rating=3)) if request.user.is_authenticated else None
			else:
				form = ReviewForm(instance=Review(course = c, user=request.user, rating=3)) if request.user.is_authenticated else None
			if len(c.reviews.all()):
				c.avg_rating = str(round(c.reviews.all().aggregate(Avg('rating'))['rating__avg'],2))+"/5"
			else:
				c.avg_rating = "N/A"
			return render(request,"courses/info.html", {'course'	:c,
														'form'		:form})

					
	# if not found, display error
	return render(request,"courses/not-found.html")
	

def search(request):
	search = request.GET.get('search', '').strip()
	c = []
	if search:
		c = list(Courses.objects.filter(name__icontains = search))
	return render(request,"courses/search.html", {'search': search, "courses": c})


def scrapeCourse(name):
	page = requests.get('https://www.handbook.unsw.edu.au/undergraduate/courses/2019/'+name)
	if page.status_code == 200:
		print("Handbook link exists works: attempting parse of html")
		try:
			soup = BeautifulSoup(page.text, 'html.parser')
			title = soup.find('span',attrs={"data-hbui":"module-title"}).get_text()
			uoc = re.match('\d+', soup.find('h4',class_="no-margin units").get_text()).group(0)
			offeringTerms = list(soup.find('div',attrs={"role":"complementary"}).descendants)[49]
			try:
				prerequisites = re.search(': (.*)',str(list(soup.find('div',id="readMoreSubjectConditions").descendants)[4])).group(1)
			except:
				prerequisites = "N/A"
			description = re.sub("\n", "\n<br><br>\n", soup.find('div',id="readMoreIntro").get_text()[:-60].strip())
			c = Courses(name=name.upper(), title=title, uoc=uoc, offeringTerms=offeringTerms, prerequisites=prerequisites, description=description)
			print("Web-scrape successful: saving data into database")
			try:
				c.save()
				return c
			except:pass
			return c
		except Exception as e:
			print("Error while scraping web page:", e)
			return None

def addCourseURLS(text, ignore=[]):
	return re.sub('\w{4}\d{4}', lambda c: '<a href="'+reverse("course_info",args=[c.group(0)])+'">'+c.group(0)+'</a>' if c.group(0) not in ignore else c.group(0), str(text))

