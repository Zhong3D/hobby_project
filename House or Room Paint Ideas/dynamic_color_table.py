from flask import Flask, request, render_template, jsonify, Response
import numpy as np
import random
from datetime import datetime
import time

app = Flask(__name__)

color_digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
dark = 0
light = 15

@app.route('/dynamic_color_table')
def dynamic_color_table():
	return render_template('dynamic_color_table.html')

@app.route('/dynamic_color_table_generator', methods = ['POST'])
def dynamic_color_table_generator():
	start = int(request.form.get('start'))
	end = int(request.form.get('end'))
	columns_qty = int(request.form.get('columns_qty'))
	max_rows = int(request.form.get('max_rows'))

	id_color_table_pairs = []
	if end <= max_rows:
		print('Adding')
		for row in range(start, end):
			id_color_row_pairs = []
			for column in range(columns_qty):
				color_code = ''
				for color_digit in range(6):
					next_color_digit = color_digits[random.randint(dark, light)]
					color_code = color_code + next_color_digit
				color_code = '#' + color_code
				cell_id = str(row * columns_qty + column)
				id_color_cell_pair = [cell_id, color_code]
				id_color_row_pairs.append(id_color_cell_pair)
			id_color_table_pairs.append(id_color_row_pairs)
	else:
		print('Modifying')
		for row in range(max_rows):
			id_color_row_pairs = []
			for column in range(columns_qty):
				color_code = ''
				for color_digit in range(6):
					next_color_digit = color_digits[random.randint(dark, light)]
					color_code = color_code + next_color_digit
				color_code = '#' + color_code
				cell_id = str(row * columns_qty + column)
				id_color_cell_pair = [cell_id, color_code]
				id_color_row_pairs.append(id_color_cell_pair)
			id_color_table_pairs.append(id_color_row_pairs)
	print('id_color_table_pairs len:' + str(len(id_color_table_pairs)))
	print('id_color_table_pairs samples: ' + str(id_color_table_pairs))
	print('id_color_table_pairs samples type: ' + str(type(id_color_table_pairs)))
	return jsonify(id_color_table_pairs)

if __name__ == '__main__':
	app.run(debug=True, use_reloader=True)
