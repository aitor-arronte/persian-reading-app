import firebase_admin
from firebase_admin import credentials, firestore
import json

cred = credentials.Certificate('creds/serviceKey.json')
firebase_admin.initialize_app(cred)

if __name__ == '__main__':
	db = firestore.client()
	collection = db.collection('words')
	docs = collection.get()
	dictionary = [{'id': d._data['id'], 'word':d._data['word']} for d in docs]
	print(json.dumps(dictionary, ensure_ascii = False), file=open('data/words.json', 'w', encoding="utf-8"))
	print(f"Dictionary file generated with {len(dictionary)} records")

