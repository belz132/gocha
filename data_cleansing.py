from functions import *
from flask import Flask, request
from flasgger import Swagger, LazyString, LazyJSONEncoder
from flasgger import swag_from
import pandas as pd

app = Flask(__name__)

app.json_encoder = LazyJSONEncoder
swagger_template = dict(
info = {
	'title': LazyString(lambda: 'API Documentation for Text Data Cleansing'),
	'version': LazyString(lambda: '0.0.1'),
	'description': LazyString(lambda: 'Dokumentasi API untuk Text Data Cleansing Dengan Input Manual dan Upload File CSV')
	},
	host = LazyString(lambda: request.host)
)
swagger_config = {
	"headers": [],
	"specs": [
		{
			"endpoint": 'docs',
			"route": '/docs.json'
		}
	],
	"static_url_path": '/flasgger_static',
	"swagger_ui": True,
	"specs_route": '/docs/'
}
swagger = Swagger(app, template=swagger_template, config=swagger_config)

# Route pertama, untuk menerima input teks dari user dan memprosesnya sesuai tipe operasi yang diinginkan user.
@swag_from("docs/text_input.yml", methods=['POST'])
@app.route('/text_input', methods=['POST'])
def text_input():
	
	# Dijalankan ketika membuat database "text_cleaning.db" dan table "tweets" untuk pertama kali.
	# conn = sqlite3.connect('text_cleaning.db')
	# conn.execute('''CREATE TABLE tweets (Input varchar(255), Operation varchar(255), Output varchar(255));''')
	# conn.close()

	text = request.form.get('Text')
	operation = request.form.get('Operation')

	# Dijalankan jika user hanya menginginkan operasi lower case.
	if operation == 'Lower Case':
		return lower_case(text, operation)

	# Dijalankan jika user hanya menginginkan operasi remove unnecessary char.
	if operation == 'Remove Unnecessary Char':
		return remove_unnecessary_char(text, operation)

	# Dijalankan jika user hanya menginginkan operasi remove non-alphanumeric char.	
	if operation == 'Remove Non-Alphanumeric Char':
		return remove_nonalphanumeric_char(text, operation)

	# Dijalankan jika user hanya menginginkan operasi normalize alay.
	if operation == 'Normalize Alay':
		return normalize_alay(text, operation)

	# Dijalankan jika user hanya menginginkan operasi remove stopword.
	if operation == 'Remove Stopword':
		return remove_stopword(text, operation)

	# Dijalankan jika user hanya menginginkan operasi stemming.
	if operation == 'Stemming':
		return stemming(text, operation)

	# Dijalankan jika user menginginkan seluruh operasi di atas.
	if operation == 'All':
		return all(text, operation)

# Route kedua, untuk menerima input file csv dari user dan memprosesnya dengan seluruh operasi.
@swag_from("docs/upfile.yml", methods=['POST'])
@app.route('/upfile', methods=['POST'])
def upfile():

	file = request.files['Upfile']

	return file_process(file)

if __name__ == '__main__':
	app.run()
