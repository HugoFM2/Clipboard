from flask import Flask, render_template, redirect, url_for, request, send_file

# import pyperclip as clipboard

from PIL import ImageGrab, ImageChops, Image
import io, base64, pyperclip


app = Flask(__name__)

@app.route('/', methods=['GET'])
def getClipboard():
	temp_img = ImageGrab.grabclipboard()
	if(temp_img is not None): # Caso o clipboard seja uma imagem
		buffer_img = io.BytesIO()
		temp_img.save(buffer_img,'PNG')
		buffer_img.seek(0)
		return	send_file(buffer_img	, mimetype='image/png')
	else: # Caso seja um texto
		return pyperclip.paste()
