from .models import *
from assessment.models import *
from django.shortcuts import render, get_list_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


@login_required
def show_material(request, level, material_id):
    reading_material = ReadingMaterial.objects.get(id=material_id, difficulty=level)
    ids = ReadingMaterial.objects.filter(difficulty=level).values_list('id').order_by('order')
    ids = [id[0] for id in ids]
    return render(request, 'reading_materials/reading.html', {'material': reading_material, 'ids': ids})


@login_required
def get_profile(request):
    profile = Profile.objects.get(user=request.user)
    responses = Responses.objects.filter(user=request.user)
    return render(request, 'reading_materials/profile.html', {'profile': profile, 'responses': responses})


def proficiency_levels(request):
    novice_ids = ReadingMaterial.objects.filter(difficulty='N').values_list('id').order_by('order')
    novice_ids = [id[0] for id in novice_ids]
    inter_ids = ReadingMaterial.objects.filter(difficulty='I').values_list('id').order_by('order')
    inter_ids = [id[0] for id in inter_ids]
    advanced_ids = ReadingMaterial.objects.filter(difficulty='A').values_list('id').order_by('order')
    advanced_ids = [id[0] for id in advanced_ids]
    init = []
    if novice_ids:
        init.append(novice_ids[0])
    else:
        init.append(0)
    if inter_ids:

        init.append(inter_ids[0])
    else:
        init.append(0)
    if advanced_ids:
        init.append(advanced_ids[0])

    return render(request, 'reading_materials/select_level.html', {'init': init})


@login_required
def save_response(request, answer_id, response):
    if request.is_ajax() and request.method=='POST':
        answer = Answer.objects.get(pk=answer_id)
        response = Responses.objects.create(answer=answer, response= response, user=request.user)
        feedback={}
        if response.answer.correct == True:
            feedback['response'] = 1
            feedback['answer'] = answer_id
        else:
            feedback['response'] = 0
            feedback['answer'] = answer_id
        return JsonResponse(feedback, content_type='application/json')

