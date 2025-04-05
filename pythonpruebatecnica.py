from flask import Flask, request

app = Flask(__name__)

@app.route('/json_a_lista', methods=['POST'])
def json_a_lista():
    json_data = request.get_json()

    # Procesar el JSON para generar la tabla
    lista = "Valor 1:{}\n".format(json_data['hardware'])
    lista += "Valor 2:{}\n".format(json_data['MessageAtt']['event_type']['event_A'])
    lista += "Valor 3:{}\n".format(json_data['MessageAtt']['traceID'])
    lista += "Valor 4:{}\n".format(json_data['Metadata']['publisher'])


    return lista

@app.route('/json_a_tabla', methods=['POST'])
def json_a_tabla():
    json_data = request.get_json()

    # Procesar el JSON para generar la tabla
    html = "<table border='1'>"
    html += "<tr><th>Valor 1</th><td>{}</td></tr>".format(json_data['hardware'])
    html += "<tr><th>Valor 2</th><td>{}</td></tr>".format(json_data['MessageAtt']['event_type']['event_A'])
    html += "<tr><th>Valor 3</th><td>{}</td></tr>".format(json_data['MessageAtt']['traceID'])
    html += "<tr><th>Valor 4</th><td>{}</td></tr>".format(json_data['Metadata']['publisher'])
    html += "</table>"

    return html

if __name__ == '__main__':
    app.run(debug=True)
