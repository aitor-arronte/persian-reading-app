from parsivar import Normalizer, Tokenizer, FindStems
from reading_materials.models import ReadingMaterial
from django.utils.html import strip_tags
import json


normalizer = Normalizer()
tokenizer = Tokenizer()
stemmer = FindStems()
word_list = open('data/words.json', 'r')
word_list = json.load(word_list)


def get_lemmas(id_last=None):
	if id:
		materials = ReadingMaterial.objects.filter(id > id_last)
	else:
		materials = ReadingMaterial.objects.all()
	for material in materials:
		wdict=[]
		words = tokenizer.tokenize_words(normalizer.normalize(strip_tags(material)))
		for word in words:
			stem = stemmer.convert_to_stem(word)
			for w in word_list:
				if stem == w['word']:
					wdict.append({'word':word, 'lemma': w['word'], 'id': w['id']})




