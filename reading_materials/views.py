from .models import *
from assessment.models import *
from django.shortcuts import render, get_list_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


@login_required
def show_material(request, level, material_id):
    reading_material = ReadingMaterial.objects.get(id=material_id, difficulty=level)
    ids = ReadingMaterial.objects.filter(difficulty=level).values_list('id').order_by('order')
    materials_passed = Progress.objects.filter(user_progress=request.user).values_list('passed_materials')
    ids = [idx[0] for idx in ids if idx[0] not in list(materials_passed)]
    return render(request, 'reading_materials/reading.html', {'material': reading_material, 'ids': ids})


@login_required
def get_profile(request):
    profile = Profile.objects.get(user=request.user)
    novice = ReadingMaterial.objects.filter(difficulty='N').count()
    intermediate = ReadingMaterial.objects.filter(difficulty='I').count()
    advanced = ReadingMaterial.objects.filter(difficulty='A').count()
    if profile.type == 'S':
        if Progress.objects.filter(user_progress=request.user, passed_materials__difficulty='N').exists():
            progress_novice = (Progress.objects.filter(user_progress=request.user, passed_materials__difficulty='N').count()/novice)*100
        else:
            progress_novice = 0
        if Progress.objects.filter(user_progress=request.user, passed_materials__difficulty='I').exists():
            progress_intermediate = (Progress.objects.filter(user_progress=request.user, passed_materials__difficulty='I').count()/intermediate)*100
        else:
            progress_intermediate = 0
        if Progress.objects.filter(user_progress=request.user, passed_materials__difficulty='A').exists():
            progress_advanced = (Progress.objects.filter(user_progress=request.user, passed_materials__difficulty='A').count()/advanced)*100
        else:
            progress_advanced = 0
        return render(request, 'reading_materials/profile.html', {'profile': profile, 'progress_novice': progress_novice, 'progress_intermediate': progress_intermediate,
                                                                 'progress_advanced':progress_advanced })
    if profile.type == 'I':
        if Progress.objects.filter(passed_materials__difficulty='N').exists():
            progress_novice = Progress.objects.filter(passed_materials__difficulty='N')
        else:
            progress_novice = None
        if Progress.objects.filter(passed_materials__difficulty='I').exists():
            progress_intermediate = Progress.objects.filter(passed_materials__difficulty='I')
        else:
            progress_intermediate = None
        if Progress.objects.filter(passed_materials__difficulty='A').exists():
            progress_advanced = Progress.objects.filter(passed_materials__difficulty='A')
        else:
            progress_advanced = None
        return render(request, 'reading_materials/profile.html',
                      {'profile': profile, 'progress_novice': progress_novice,
                       'progress_intermediate': progress_intermediate,
                       'progress_advanced': progress_advanced, 'n_profile':profile, 'n_intermediate':intermediate, 'n_advanced': advanced})


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
def save_responses(request):
    if request.is_ajax() and request.method=='POST':
        answers =  request.POST.getlist("responses[]", None)
        material_id = request.POST.get("material_id", None)
        feedback = {}
        correct=0
        for ans in answers:
            answer = Answer.objects.get(pk=ans)
            response = Responses.objects.create(answer=answer, user=request.user)
            if response.answer.correct == True:
                correct+=1
                feedback['response'] = 1
                feedback['question'] = answer.question.content
            else:
                feedback['response'] = 0
                feedback['answer'] = answer.question.content
        if correct == len(answers):
            progress=Progress.objects.create()
            progress.user_progress.add(request.user)
            progress.passed_materials.add(ReadingMaterial.objects.get(id=material_id))
            print(feedback)
        return JsonResponse(feedback, content_type='application/json')