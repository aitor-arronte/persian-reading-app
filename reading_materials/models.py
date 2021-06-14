from django.db import models
from django.contrib.auth.models import User
import random
from assessment.models import Quiz


difficulty_options =(
	('N', 'Novice'),
	('I', 'Intermediate'),
	('A', 'Advanced')
)



class ReadingMaterial(models.Model):
	instructions = models.TextField(blank=False)
	title = models.CharField(max_length=256, blank=False, verbose_name='Reading number')
	audio = models.FileField(blank=True, upload_to='uploads/')
	difficulty = models.CharField(max_length=1, choices=difficulty_options, blank=False)
	order = models.IntegerField(default=1)
	video = models.FileField(blank=True, upload_to='uploads/')
	image = models.ImageField(blank=True, upload_to='uploads/')
	pdf = models.FileField(blank=True, upload_to='uploads/')
	text = models.TextField(
		blank=True,
		help_text=("Reading text"),
	)
	quizzes = models.ManyToManyField(Quiz, blank=True)


	class Meta:
		ordering = ['order']

	def __str__(self):
		return str(self.title)