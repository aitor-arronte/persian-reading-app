from .models import *
from assessment.models import *
from django.shortcuts import render, get_list_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from parsivar import Normalizer, Tokenizer, FindStems
from reading_materials.models import ReadingMaterial, WordDictionary
from django.utils.html import strip_tags
import json
import argparse


normalizer = Normalizer()
tokenizer = Tokenizer()
stemmer = FindStems()
word_list = open('data/words.json', 'r')
word_list = json.load(word_list)
parser = argparse.ArgumentParser()


@login_required
def show_material(request, level, material_id):
    reading_material = ReadingMaterial.objects.get(id=material_id, difficulty=level)
    words = WordDictionary.objects.get(material=reading_material)
    ids = ReadingMaterial.objects.filter(difficulty=level).values_list('id').order_by('order')
    materials_passed = Progress.objects.filter(user_progress=request.user)
    materials_passed = set(material.id for material in materials_passed)
    ids = [idx[0] for idx in ids if idx[0] not in materials_passed]
    return render(request, 'reading_materials/reading.html', {'material': reading_material, 'ids': ids, 'words': words})


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


@login_required
def proficiency_levels(request):
    materials_passed = Progress.objects.filter(user_progress=request.user).values('passed_materials')
    materials_passed = set(material['passed_materials'] for material in materials_passed)
    novice_ids = ReadingMaterial.objects.filter(difficulty='N').values_list('id').order_by('order')
    novice_ids = [id[0] for id in novice_ids if id[0] not in materials_passed]
    inter_ids = ReadingMaterial.objects.filter(difficulty='I').values_list('id').order_by('order')
    inter_ids = [id[0] for id in inter_ids if id[0] not in materials_passed]
    advanced_ids = ReadingMaterial.objects.filter(difficulty='A').values_list('id').order_by('order')
    advanced_ids = [id[0] for id in advanced_ids if id[0] not in materials_passed]
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
    else:
        init.append(0)
    return render(request, 'reading_materials/select_level.html', {'init': init})


@login_required
def save_responses(request):
    if request.is_ajax() and request.method=='POST':
        answers =  request.POST.getlist("responses[]", None)
        material_id = request.POST.get("material_id", None)
        user = User.objects.get(username=request.user)
        output=[]
        correct=0
        for ans in answers:
            feedback = {}
            answer = Answer.objects.get(pk=ans)
            response = Responses.objects.create(answer=answer, user=request.user)
            if response.answer.correct == True:
                correct+=1
                feedback['result'] = 1
                feedback['response'] = 'is correct'
                feedback['answer'] = answer.content
                feedback['question'] = answer.question.content
                output.append(feedback)
            else:
                feedback['result'] = 0
                feedback['response'] = 'is incorrect'
                feedback['answer'] = answer.content
                feedback['question'] = answer.question.content
                output.append(feedback)
        if correct == len(answers):
            if not Progress.objects.filter(user_progress=user).exists():
                progress=Progress.objects.create(user_progress=user)
                progress.passed_materials.add(ReadingMaterial.objects.get(id=material_id))
            else:
                progress = Progress.objects.get(user_progress=user)
                progress.passed_materials.add(ReadingMaterial.objects.get(id=material_id))
        return JsonResponse(output, content_type='application/json', safe=False)


@login_required
def create_entries(request):
    existing = WordDictionary.objects.all().values('material')
    existing = [e['material'] for e in existing]
    word_dictionary=[]
    materials = ReadingMaterial.objects.all()
    for material in materials:
        if material.id not in existing:
            wdict=[]
            words = tokenizer.tokenize_words(normalizer.normalize(strip_tags(material.text)))
            material_object = ReadingMaterial.objects.get(id=material.id)
            for word in words:
                stem = stemmer.convert_to_stem(word)
                for w in word_list:
                    if stem == w['word']:
                        if {'word':word, 'stem': w['word'], 'id': w['id']} not in wdict:
                            wdict.append({'word':word, 'stem': w['word'], 'id': w['id']})
            word_dictionary.append(WordDictionary(material=material_object, dictionary=wdict))
    try:
        if len(wdict) >0:
            WordDictionary.objects.bulk_create(word_dictionary)
            return HttpResponse("Created stem for dictionary.")
        else:
            return HttpResponse("No entries added.")
    except:
        return HttpResponse("There has been an error with stemming.")