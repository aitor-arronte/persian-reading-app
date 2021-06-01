from .models import *
from django.shortcuts import render, get_list_or_404


def show_material(request, level, material_id):
    reading_material = ReadingMaterial.objects.get(id=material_id, difficulty=level)
    ids = ReadingMaterial.objects.filter(difficulty=level).values_list('id').order_by('order')
    ids = [id[0] for id in ids]
    return render(request, 'reading_materials/reading_material.html', {'material': reading_material, 'ids': ids})


def proficiency_levels(request):
    novice_ids = ReadingMaterial.objects.filter(difficulty='N').values_list('id').order_by('order')
    novice_ids = [id for id in novice_ids]
    inter_ids = ReadingMaterial.objects.filter(difficulty='I').values_list('id').order_by('order')
    inter_ids = [id[0] for id in inter_ids]
    advanced_ids = ReadingMaterial.objects.filter(difficulty='A').values_list('id').order_by('order')
    advanced_ids = [id for id in advanced_ids]
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


def get_reading_materials(request, level):
    cards_list=[]
    cards = get_list_or_404(ReadingMaterial, difficulty=level)
    for c in cards:
        card={}
        card['id'] = c.pk
        card['title'] = c.title
        card['text'] = c.text
        card['description'] = c.description
        if c.image:
            card['image'] = c.image.url
        elif c.video:
            card['video'] = c.video
        elif c.audio:
            card['audio'] = c.audio
        try:
            card['options'] =[]
            for o in c.get_answers():
                card['options'] += o
        except:
            card['quizzes']=''
        cards_list.append(card)

    return render(request, 'reading_materials/reading_material.html', {'cards': cards_list })
