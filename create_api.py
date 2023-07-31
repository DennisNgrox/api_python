from flask import Flask, jsonify, request
import json
import shutil
import tempfile
import os


# Definir diretório do programa --- \\ EDITAR O DIRETORIO AONDE SE ENCONTRA O PROGRAMA
diretorio_programa = 'C:\\Desktop'

diretorio_script = os.path.dirname(os.path.abspath(__file__))
os.chdir(diretorio_programa)

app = Flask(__name__)

with open('sqlite.json', 'r', encoding='utf8') as f:
    dados = json.load(f)

# Get total de dados
@app.route('/dados')
def pag_inicial():
    return dados

# Get por id
@app.route('/dados/<int:id>', methods=['GET'])
def get_dados(id):
    try:
        with open('sqlite.json', 'r', encoding='utf8') as f:
            getDados = json.load(f)
            for indice, value in enumerate(getDados):
                if value.get('id') == id:
                    found_data = getDados[indice]
                    return jsonify(found_data)

            return jsonify({"message": "id invalido"})

    except TypeError:
        return jsonify('invalid')

# Adicionar dados
@app.route('/dados', methods=['POST'])
def criar_dados():
    with open('sqlite.json', 'r', encoding='utf8') as f:
        newDados = json.load(f)

    newValue = request.get_json()
    newDados.append(newValue)

    with tempfile.NamedTemporaryFile('w', delete=False) as out:
        json.dump(newDados, out, ensure_ascii=False,
                  indent=4, separators=(',', ':'))

    shutil.move(
        out.name, 'sqlite.json')
    return jsonify(newDados)


# Editar dados por id
@app.route('/dados/<int:id>', methods=['PUT'])
def editar_dados(id):
    with open('sqlite.json', 'r', encoding='utf8') as f:
        editing_dados = json.load(f)
        editValue = request.get_json()
        for indice, valor in enumerate(editing_dados):
            if valor.get('id') == id:
                editing_dados[indice].update(editValue)

        with tempfile.NamedTemporaryFile('w', delete=False) as out:
            json.dump(editing_dados, out, ensure_ascii=False,
                      indent=4, separators=(',', ':'))

        shutil.move(
            out.name, 'sqlite.json')
        return jsonify(editing_dados)


# Deletar dados
@app.route('/dados/<int:id>', methods=['DELETE'])
def deletar_dado(id):
    with open('sqlite.json', 'r', encoding='utf8') as f:
        deleting_dados = json.load(f)
        for indice, valor in enumerate(deleting_dados):
            if valor.get('id') == id:
                del deleting_dados[indice]

    with tempfile.NamedTemporaryFile('w', delete=False) as out:
        json.dump(deleting_dados, out, ensure_ascii=False,
                  indent=4, separators=(',', ':'))

    shutil.move(out.name, 'sqlite.json')
    return jsonify(deleting_dados)


app.run(port=5000, host='localhost', debug=True)
