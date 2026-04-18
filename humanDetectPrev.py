from flask import Flask, request
app = Flask(__name__)

@app.route('/foto', methods=['POST'])
def recibir_foto():
    with open('foto.jpg', 'wb') as f:
        f.write(request.data)
    print("Foto guardada")
    return 'OK', 200

app.run(host='0.0.0.0', port=5000)