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


def get_lemmas(id_last=None):
	word_dictionary=[]
	if id:
		materials = ReadingMaterial.objects.filter(id > id_last)
	else:
		materials = ReadingMaterial.objects.all()
	for material in materials:
		wdict=[]
		words = tokenizer.tokenize_words(normalizer.normalize(strip_tags(material)))
		material_object = ReadingMaterial.objects.get(id=material.id)
		for word in words:
			stem = stemmer.convert_to_stem(word)
			for w in word_list:
				if stem == w['word']:
					wdict.append({'word':word, 'lemma': w['word'], 'id': w['id']})
		word_dictionary.append(WordDictionary(material=material_object, dictionary=wdict))
	WordDictionary.objects.bulk_create(word_dictionary)
	return None


if __name__ == 'main':
	parser.add_argument('-id', '--last_id', type=int, default=40,
	                    help='Last id')

	args = parser.parse_args()

	if args.last_id:
		get_lemmas(id_last=args.last_id)
	else:
		get_lemmas()