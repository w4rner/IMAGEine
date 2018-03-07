from django.db import models

# Create your models here.
class Landmark(models.Model):
	i_d = models.IntegerField(default=0)
	name = models.CharField(max_length=200)
	photo = models.CharField(max_length=200)
	wiki_url = models.CharField(default='',max_length=200)
	wiki_sum = models.CharField(default='',max_length=3000)

	def __str__(self):
		return self.name

class Choice(models.Model):
	landmark = models.ForeignKey(Landmark, on_delete=models.CASCADE)
	name = models.CharField(max_length=200)
	correct = models.BooleanField()
	machine = models.BooleanField()
	#machine confidence
	guess = models.BooleanField(default = False)

	def __str__(self):
		return self.name
