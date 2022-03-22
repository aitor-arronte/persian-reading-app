# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
import datetime
from django.utils.html import strip_tags


languages =(
	('E', 'English'),
	('P', 'Persian')
)


class Quiz (models.Model):
    name = models.CharField(max_length=150, blank=False)

    def get_questions(self):
      questions = Question.objects.filter(quiz=self)
      return questions

    class Meta:
        verbose_name = _ ("Quiz")
        verbose_name_plural = _ ("Quizzes")

    def __str__(self):
        return strip_tags(self.name)


class Question(models.Model):

    quiz = models.ManyToManyField(Quiz,
                                  verbose_name=_("Quiz"),
                                  blank=True)

    content = models.TextField(
                               blank=False,
                               help_text=_("Enter the question text that "
                                           "you want to be displayed"),
                               verbose_name=_('Question'))
    language = models.CharField(max_length=1, choices=languages, blank=False, default='P')

    class Meta:
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")

    def __str__(self):
      return "Question: " + strip_tags(self.content)



    def check_if_correct(self, guess):
        answer = Answer.objects.get (id=guess)

        if answer.correct is True:
            return True
        else:
            return False

    def get_answers(self):
        return Answer.objects.filter(question=self)

    def get_answers_list(self):
        return [(answer.id, answer.content) for answer in
                self.Answer.objects.filter (question=self)]

    def answer_choice_to_string(self, guess):
        return Answer.objects.get(id=guess).content



class Answer(models.Model):

    question = models.ForeignKey(Question, verbose_name=_("Question"), on_delete=models.CASCADE)

    content = models.TextField(
                               blank=False,
                               help_text=_("Enter the answer text that "
                                           "you want displayed"),
                               verbose_name=_("Content"))

    correct = models.BooleanField(blank=False,
                                  default=False,
                                  help_text=_("Is this a correct answer?"),
                                  verbose_name=_("Correct"))

    class Meta:
        verbose_name = _("Answer")
        verbose_name_plural = _("Answers")


    def get_responses(self):
        users = User.objects.exclude(id__in=(1, 2, 3))
        responses = Responses.objects.filter(answer=self, user__in=users)
        return responses

    def get_user_responses(self, users):
        responses = Responses.objects.filter(answer=self, user__in=users)
        return responses

    def __str__(self):
        return self.content

    def __str__(self):
      return strip_tags(self.content)


class Responses(models.Model):
  answer = models.ForeignKey('Answer', on_delete=models.CASCADE)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  created = models.DateTimeField(default=datetime.datetime.now())

  def __str__(self):
    return self.user.username+' response'

class Attempt(models.Model):
  responses= models.ManyToManyField(Responses)
  created = models.DateTimeField(default=datetime.datetime.now())
  closed = models.BooleanField(default=False)