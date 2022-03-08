from .models import *
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


@login_required
def save_quiz_response(request, choice_id, sequence_id):
    if request.is_ajax() and request.method=='POST':
        answer = Answer.objects.get(pk=choice_id)
        response = QuestionRating.objects.create(answer=answer, user=request.user)
        card_sequence = CardSequence.objects.get(pk=sequence_id)
        card_sequence.quiz_responses.add(response)
        card_sequence.save()
        return HttpResponse(response.pk)

@login_required
def get_quizscore_sequence(request, sequence_id):
    print(sequence_id)
    seq = CardSequence.objects.get(pk=sequence_id)
    score=0
    if len(seq.quiz_responses.all())>0:
        for correct in seq.quiz_responses.all():
            score+= int(correct.answer.correct)
        percent = score/len(seq.quiz_responses.all())
        return HttpResponse(str(percent*100)+ ' % correct in your quizzes')
    else:
        return HttpResponse("Topic completed.")




