from flask import Flask, request, jsonify, render_template, send_file
from rdflib import Graph, ConjunctiveGraph, RDF, RDFS, OWL, URIRef
import os
import morph_kgc

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'trig'}
app.config['MAPPING_FILE_PATH'] = "mapping/mapping_file.rml.ttl"
app.config['MAPPING_FILE'] = """
            [DataSource]
            mappings: $mapping_file
            file_path: $file_path
         """

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

data_list = []
processed_data_list = []

@app.route('/upload_data', methods=['POST'])
def upload_data():
    global data_list
    if 'file' not in request.files:
        return jsonify(status="failure", message="No file part"), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify(status="failure", message="No selected file"), 400

    if file and allowed_file(file.filename):
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        data_list.append(file.filename)
        return jsonify(status="success", message="File uploaded successfully"), 200
    else:
        return jsonify(status="failure", message="File type not allowed"), 400

@app.route('/process_data', methods=['GET'])
def process_data():
    global data_list, processed_data_list
    # processed_data_list = [item[::-1] for item in data_list]
    result = "temp_result.ttl"
    g = ConjunctiveGraph()


    for item in data_list:
        path = os.getcwd()+"/uploads/"+item
        print(path)

        g.parse(path, format="trig")

        # get the ontology construct needed to build the resulted KG
        ontology_named_graph = URIRef("http://example.org/test/AlloyDataset_Ontology")
        ontology_graph = g.get_context(ontology_named_graph)

        # get the RML mapping for transformation and store it in the designated path
        mapping_named_graph = URIRef("http://example.org/test/AlloyDataset_TriplesMap")
        rml_mapping = g.get_context(mapping_named_graph)
        rml_mapping.serialize(destination=app.config['MAPPING_FILE_PATH'])

        # get the location of downloadURL from DCAT and appent to the config file
        morph_config = app.config['MAPPING_FILE']
        morph_config = morph_config.replace("$mapping_file", app.config['MAPPING_FILE_PATH'])
        # dcat = g.get_context()
        print(morph_config)
        # print(dcat)
        downloadURL = URIRef("http://www.w3.org/ns/dcat#downloadURL")
        for s, p, o in g.triples((None, downloadURL, None)):
            print(f"{s} {p} {o}")
            morph_config = morph_config.replace("$file_path", o)
        print(morph_config)
        
        # start transformation
        resulted_graph = morph_kgc.materialize(morph_config)
        for ns_prefix, namespace in g.namespaces():
            resulted_graph.namespace_manager.bind(ns_prefix, namespace)
        resulted_graph += ontology_graph
        resulted_graph.serialize(destination=result)

    data_list = []
    processed_data_list.append(result)
    return jsonify(status="success", message="Data processed successfully"), 200

@app.route('/store_data', methods=['GET'])
def store_data():
    global processed_data_list
    if not processed_data_list:
        return jsonify(status="failure", message="No data to store"), 400
    
    result = None
    for item in processed_data_list:
        result = item
    processed_data_list = []

    return send_file(item, as_attachment=True, max_age=0)
    

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)