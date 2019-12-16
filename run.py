from flask import Flask
from flask import render_template, request, Flask
from werkzeug import secure_filename
import os

from rsa.rsa import RSA

app = Flask(__name__)
ALLOWED_EXTENSIONS = set(['txt'])

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        upload_data = request.files['file']

        if upload_data and allowed_file(upload_data.filename):
            filename = secure_filename(upload_data.filename)
            app.config['UPLOAD_FOLDER'] = 'upload'
            upload_data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            with open('upload/plaintext.txt', 'rt') as f:
                data = f.read()

            print('Plain text:{}'.format(data))
            rsa = RSA(data)
            public_key, private_key, encrypted_message = rsa.encrypt()
            print(public_key)
            print(private_key)
            print('Encrypted message:{}'.format(encrypted_message))
            decrypted_message = rsa.decrypt()
            print('Decrypted message:{}'.format(decrypted_message))

            return render_template('data.html', plain=data, encrypted_message=encrypted_message,
            public_key=public_key, private_key=private_key, decrypted_message=decrypted_message)
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run()