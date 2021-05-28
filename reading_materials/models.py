from django.db import models
import datetime
from django.contrib.auth.models import User
from django.utils.timezone import now
import random


difficulty_options =(
	('N', 'Novice'),
	('I', 'Intermediate'),
	('A', 'Advanced')
)

quiz_options=(
	('M', 'Matching'),
	('S', 'Single choice')
)


class ReadingMaterial(models.Model):
	rubric = models.TextField(blank=False)
	title = models.CharField(max_length=155, blank=False)
	audio = models.FileField(blank=True, upload_to='uploads/')
	difficulty = models.CharField(max_length=1, choices=difficulty_options, blank=False)
	order = models.IntegerField(default=1)
	video = models.FileField(blank=True, upload_to='uploads/')
	image = models.ImageField(blank=True, upload_to='uploads/')
	quiz_type = models.CharField(max_length=1, choices=quiz_options, default='S')
	quiz_instructions = models.TextField(blank=True, verbose_name='Quiz instructions')
	use_glossing = models.BooleanField(blank=False, default=False)


	class Meta:
		ordering = ['order']

	def get_answers(self):
		answers = Answer.objects.filter(material=self)
		answers = sorted(answers, key=lambda x: random.random())
		return answers

	def get_options(self):
		answer_option = Answer.objects.filter(material=self).values('option')
		words = sorted(answer_option , key=lambda x: random.random())
		return words

	def get_results(self):
		answer_result = Answer.objects.filter(material=self).values('result')
		results = sorted(answer_result, key=lambda x: random.random())
		return results

	def get_texts(self):
		texts = ReadingText.objects.filter(material=self)
		texts = sorted(texts, key=lambda x: random.random())
		return texts

	def __str__(self):
		return str(self.title)


class ReadingText(models.Model):
	material = models.ForeignKey(ReadingMaterial, verbose_name=("Reading Material"), on_delete=models.CASCADE)
	text = models.TextField(
			blank=True,
			help_text=("Reading text"),
		)

	gloss = models.TextField(
			blank=True,
			help_text=("Gloss"),
			verbose_name=("Gloss for the text "))



class Answer(models.Model):
		material = models.ForeignKey(ReadingMaterial, verbose_name=("Reading Material"), on_delete=models.CASCADE)
		option = models.CharField(max_length=255,
																blank=False,
																help_text=("Enter the answer text that "
																						 "you want displayed"),
																verbose_name=("Content"))
		result = models.CharField(max_length=255, verbose_name='Response or feedback', blank=True)

		correct = models.BooleanField(default=False, blank=False)


		def get_responses(self):
				users = User.objects.exclude(id__in=(1))
				responses = Response.objects.filter(answer=self, user__in=users)
				return responses

		def get_user_responses(self, users):
				responses = Response.objects.filter(answer=self, user__in=users)
				return responses

		def __str__(self):
				return self.material.title+" "+self.option

		class Meta:
				verbose_name = ("Quiz")
				verbose_name_plural = ("Quizzes")



class Response(models.Model):
	option = models.ForeignKey('Answer', on_delete=models.CASCADE)
	start_time = models.DateTimeField()
	end_time = models.DateTimeField(default=now)
	user = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return str(self.option.name)