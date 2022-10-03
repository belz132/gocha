import re
import pandas as pd
from flask import jsonify
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import sqlite3
from datetime import datetime as dt

factory = StemmerFactory()
stemmer = factory.create_stemmer()

alay_dict = pd.read_csv('new_kamusalay.csv', encoding='latin-1', header=None)
alay_dict = alay_dict.rename(columns={0: 'original', 1: 'replacement'})
alay_dict_map = dict(zip(alay_dict['original'], alay_dict['replacement']))

id_stopword_dict = pd.read_csv('stopwordbahasa.csv', header=None)
id_stopword_dict = id_stopword_dict.rename(columns={0: 'stopword'})

def lower_case(text, operation):
	
	input = text
	op = operation
	output = text.lower()

	json_response = {
		'status_code': 200,
		'description': "Teks dengan format lower case",
		'data': output
	}
	
	# Membuat koneksi ke database "text_cleaning.db" dan memasukkan data input, jenis operasi dan outputnya ke table "tweets".
	conn = sqlite3.connect('text_cleaning.db')
	conn.execute("INSERT INTO tweets VALUES (?, ?, ?)", (input, op, output))
	conn.commit()
	conn.close()
	
	response_data = jsonify(json_response)
	return response_data

def remove_unnecessary_char(text, operation):

	input = text
	op = operation
	output = re.sub('\n', ' ', text)
	output = re.sub('rt', ' ', output)
	output = re.sub('user', ' ', output)
	output = re.sub(r'((www\.[^\s]+)|(http?://[^\s]+)|(https?://[^\s]+))', ' ', output)
	output = re.sub(' +', ' ', output)
	
	json_response = {
		'status_code': 200,
		'description': "Teks tanpa unnecessary character",
		'data': output
	}

	# Membuat koneksi ke database "text_cleaning.db" dan memasukkan data input, jenis operasi dan outputnya ke table "tweets".
	conn = sqlite3.connect('text_cleaning.db')
	conn.execute("INSERT INTO tweets VALUES (?, ?, ?)", (input, op, output))
	conn.commit()
	conn.close()

	response_data = jsonify(json_response)
	return response_data

def remove_nonalphanumeric_char(text, operation):

	input = text
	op = operation
	output = re.sub('[^a-zA-Z0-9]+', ' ', text)

	json_response = {
		'status_code': 200,
		'description': "Teks tanpa non-alphanumeric character",
		'data': output
	}

	# Membuat koneksi ke database "text_cleaning.db" dan memasukkan data input, jenis operasi dan outputnya ke table "tweets".
	conn = sqlite3.connect('text_cleaning.db')
	conn.execute("INSERT INTO tweets VALUES (?, ?, ?)", (input, op, output))
	conn.commit()
	conn.close()

	response_data = jsonify(json_response)
	return response_data

def normalize_alay(text, operation):

	input = text
	op = operation
	output = ' '.join([alay_dict_map[word] if word in alay_dict_map else word for word in text.split(' ')])

	json_response = {
		'status_code': 200,
		'description': "Teks yang telah dinormalisasi",
		'data': text
	}

	# Membuat koneksi ke database "text_cleaning.db" dan memasukkan data input, jenis operasi dan outputnya ke table "tweets".
	conn = sqlite3.connect('text_cleaning.db')
	conn.execute("INSERT INTO tweets VALUES (?, ?, ?)", (input, op, output))
	conn.commit()
	conn.close()

	response_data = jsonify(json_response)
	return response_data

def remove_stopword(text, operation):

	input = text
	op = operation
	output = ' '.join(['' if word in id_stopword_dict.stopword.values else word for word in text.split(' ')])
	output = output.strip()

	json_response = {
		'status_code': 200,
		'description': "Teks tanpa stopword",
		'data': text
	}

	# Membuat koneksi ke database "text_cleaning.db" dan memasukkan data input, jenis operasi dan outputnya ke table "tweets".
	conn = sqlite3.connect('text_cleaning.db')
	conn.execute("INSERT INTO tweets VALUES (?, ?, ?)", (input, op, output))
	conn.commit()
	conn.close()

	response_data = jsonify(json_response)
	return response_data

def stemming(text, operation):

	input = text
	op = operation
	output = stemmer.stem(text)
	json_response = {
		'status_code': 200,
		'description': "Teks yang telah di-stem",
		'data': output
	}

	# Membuat koneksi ke database "text_cleaning.db" dan memasukkan data input, jenis operasi dan outputnya ke table "tweets".
	conn = sqlite3.connect('text_cleaning.db')
	conn.execute("INSERT INTO tweets VALUES (?, ?, ?)", (input, op, output))
	conn.commit()
	conn.close()

	response_data = jsonify(json_response)
	return response_data

def all(text, operation):

	input = text
	op = operation

	# Lower Case Operation
	output = text.lower()

	# Removing Unnecessary Characters
	output = re.sub('\n', ' ', output)
	output = re.sub('rt', ' ', output)
	output = re.sub('user', ' ', output)
	output = re.sub(r'((www\.[^\s]+)|(http?://[^\s]+)|(https?://[^\s]+))', ' ', output)
	output = re.sub(' +', ' ', output)

	# Removing Non-Alphanumeric Characters
	output = re.sub('[^a-zA-Z0-9]+', ' ', output)

	# Normalizing Alay Words
	output = ' '.join([alay_dict_map[word] if word in alay_dict_map else word for word in output.split(' ')])

	# Removing Stopword
	output = ' '.join(['' if word in id_stopword_dict.stopword.values else word for word in output.split(' ')])
	output = output.strip()

	# Stemming
	output = stemmer.stem(output)
		
	json_response = {
		'status_code': 200,
		'description': "Teks yang telah dibersihkan secara keseluruhan",
		'data': output
	}

	# Membuat koneksi ke database "text_cleaning.db" dan memasukkan data input, jenis operasi dan outputnya ke table "tweets".
	conn = sqlite3.connect('text_cleaning.db')
	conn.execute("INSERT INTO tweets VALUES (?, ?, ?)", (input, op, output))
	conn.commit()
	conn.close()		

	response_data = jsonify(json_response)
	return response_data

def file_process(file):

	# Membuat dataframe dari file csv yang diinput user.
	file_df = pd.read_csv(file, encoding='ISO-8859-1')

	# Membuat list "cleaned_tweet" yang akan menampung hasil pembersihan setiap teks di kolom "Tweet" pada dataframe, sebelum di assign ke kolom baru yang dinamakan "Cleaned_Tweet".
	cleaned_tweet = []
 
	# Membuat list "response_data" yang akan menampung "json_response" dari setiap hasil pemprosesan teks, sebelum di display pada tampilan swagger.
	response_data =  []

	# Membuat variabel-variabel untuk kebutuhan menampilan waktu lokal (komputer). Waktu lokal inilah yang akan digunakan sebagai format nama setiap file baru dari hasil pemrosesan file input. 
	curr_time = dt.now()
	d = curr_time.day
	mo = curr_time.month
	y = curr_time.year
	h = curr_time.hour
	mi = curr_time.minute
	s = curr_time.second

	# Loop untuk mengiterasi setiap cell teks di kolom "Tweet" dan memprosesnya.
	for ind in file_df.index:

		text = file_df['Tweet'][ind]

		# Lower Case Operation
		text = text.lower()

		# Removing Unnecessary Characters
		text = re.sub('\n', ' ', text)
		text = re.sub('rt', ' ', text)
		text = re.sub('user', ' ', text)
		text = re.sub(r'((www\.[^\s]+)|(http?://[^\s]+)|(https?://[^\s]+))', ' ', text)
		text = re.sub(' +', ' ', text)

		# Removing Non-Alphanumeric Characters
		text = re.sub('[^a-zA-Z0-9]+', ' ', text)

		# Normalizing Alay Words
		text = ' '.join([alay_dict_map[word] if word in alay_dict_map else word for word in text.split(' ')])

		# Removing Stopword
		text = ' '.join(['' if word in id_stopword_dict.stopword.values else word for word in text.split(' ')])
		text = text.strip()

		# Stemming
		text = stemmer.stem(text)
		
		json_response = {
		'status_code': 200,
		'description': "Teks yang telah dibersihkan secara keseluruhan",
		'data': text
		}		
	
		cleaned_tweet.append(text)
		response_data.append(json_response)

	# Membuat kolom baru pada dataframe dengan nama "Cleaned_Tweet" dan diisi dengan data dari list "cleaned_tweet" yg isinya hasil pembersihan setiap iterasi teks di di atas.
	file_df['Cleaned_Tweet'] = cleaned_tweet
 
	# Membuat dataframe baru dengan nama "tweet_df" yang berisi 2 kolom yakni "Tweet" dan "Cleaned_Tweet"
	tweet_df = file_df[['Tweet', 'Cleaned_Tweet']]
 
	# Mengeksport dataframe "tweet_df" ke file csv baru yg dinamakan sesuai dengan format waktu lokal (komputer).
	tweet_df.to_csv(f"{d}_{mo}_{y}_{h}_{mi}_{s}.csv", index=False)

	return response_data
