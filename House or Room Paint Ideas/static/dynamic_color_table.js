document.addEventListener('DOMContentLoaded', load);

let counter = 0;
const interval = 50;
const columns_qty = 10;
const max_rows = 50;

const cell_width = '100px';
const cell_height = '50px';


function load() {
	window.onclick = () => {
		let start = counter;
		const end = start + interval;
		counter = end;

		const request = new XMLHttpRequest();
		request.open('POST', '/dynamic_color_table_generator');

		request.onload = () => {
			const data = JSON.parse(request.responseText);
			console.log('Received data from server: ' + data);
			if (end > max_rows) {
				modify_color(data);
			}
			else
				data.forEach(add_color);
		};
		const data = new FormData();
		data.append('start', start);
		data.append('end', end);
		data.append('columns_qty', columns_qty);
		data.append('max_rows', max_rows);
		console.log('Data sent to server: start of ' + data.get('start'));
		request.send(data);
		return false;
	}

}


function add_color(row_info) {
	console.log('Row_info: ' + row_info);
	const tr = document.createElement('tr');
	tr.className = 'row';
	for (let i = 0; i < columns_qty; i++) {
		const td = document.createElement('td');
		td.className = 'color_cell';
		td.id = 'C_' + row_info[i][0];
		td.innerHTML = row_info[i][1];
		td.style.color = row_info[i][1];
		td.style.background = row_info[i][1];
		td.style.width = cell_width;
		td.style.height = cell_height;
		tr.append(td);
	document.querySelector('#main_table').append(tr);
	}

}

function modify_color(row_info) {
	for (let i = 0; i < row_info.length; i++) {
		for (let j = 0; j < columns_qty; j++) {
			document.querySelector('#C_' + row_info[i][j][0]).style.background = row_info[i][j][1];
			text_color = row_info[i][j][1]
			document.querySelector('#C_' + row_info[i][j][0]).innerHTML = text_color;
			document.querySelector('#C_' + row_info[i][j][0]).style.color = text_color;
		};
	};

	$('.color_cell').on({
		mouseenter: function () {
			td_color = $(this).css('color');
			td_id = $(this).attr('id');
			td_id_row = Math.floor(td_id.split('_')[1] / columns_qty)
			td_id_col = td_id.split('_')[1] % columns_qty;
			ori_cell_color = row_info[td_id_row][td_id_col][1];
			red = parseFloat(hexToRgb(ori_cell_color)['r']);
			green = parseFloat(hexToRgb(ori_cell_color)['g']);
			blue = parseFloat(hexToRgb(ori_cell_color)['b']);
			console.log(red, green, blue);
			hsv = rgb2hsv(red, green, blue);
			console.log(hsv);
			if (hsv['v'] > 1 / 2) {
				shown_color = '#000000';
			}
			else {
				shown_color = '#ffffff';
			};

			$(this).css('color', shown_color);
		},
		mouseleave: function () {
			$(this).css('color', ori_cell_color);
		}    
	});
}

function hexToRgb(hex) {
	var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
	return result ? {
		r: parseInt(result[1], 16),
		g: parseInt(result[2], 16),
		b: parseInt(result[3], 16)
	} : null;
}

function rgb2hsv (r, g, b) {
	let rabs, gabs, babs, rr, gg, bb, h, s, v, diff, diffc, percentRoundFn;
	rabs = r / 255;
	gabs = g / 255;
	babs = b / 255;
	v = Math.max(rabs, gabs, babs),
	diff = v - Math.min(rabs, gabs, babs);
	diffc = c => (v - c) / 6 / diff + 1 / 2;
	percentRoundFn = num => Math.round(num * 100) / 100;
	if (diff == 0) {
		h = s = 0;
	} else {
		s = diff / v;
		rr = diffc(rabs);
		gg = diffc(gabs);
		bb = diffc(babs);

		if (rabs === v) {
			h = bb - gg;
		} else if (gabs === v) {
			h = (1 / 3) + rr - bb;
		} else if (babs === v) {
			h = (2 / 3) + gg - rr;
		}
		if (h < 0) {
			h += 1;
		}else if (h > 1) {
			h -= 1;
		}
	};
	return {
		h: Math.round(h * 360),
		s: percentRoundFn(s),
		v: percentRoundFn(v)
	}
}
