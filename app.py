from flask import Flask,request, send_file
from PIL import ImageGrab, Image
import io,  pyperclip
import win32clipboard



app = Flask(__name__)


def send_to_clipboard(clip_type, data):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(clip_type, data)
    win32clipboard.CloseClipboard()


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


@app.route('/uploader',methods =['POST'])
def success():
	if request.method == 'POST':  
		f = request.files['file']
		f = request.files.get('file', None)	

		image = Image.open(f)

		output = io.BytesIO()
		new_image = Image.new("RGBA", image.size, "WHITE") # Colocar fundo branco em pngs transparentes
		new_image.paste(image, mask=image)
		new_image.convert("RGB").save(output, "BMP")
		data = output.getvalue()[14:]
		output.close()
		send_to_clipboard(win32clipboard.CF_DIB, data) 
		return 'Sucesso!'



	

