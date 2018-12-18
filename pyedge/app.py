# NOTE: How about using hdf5 to store the data (compressed and encrypted?)

from flask import Flask, request, jsonify
import sys
from Edge import Node 

app = Flask(__name__)
node = None

edgeNodes = ['127.0.0.1:5005',
             '127.0.0.1:8000']

edgeIndex = [{'README.txt': [{'ip': '127.0.0.1:5005',
                              'ip': '127.0.0.1:5008'}]},
              {'.gitignore': [{'ip': '32.233.44.56:8000'}]}
                               
             ]

@app.route('/')
def index():
    return jsonify(index=edgeIndex,
                   nodes=node.node_list)


"""
Respond to an 'r u alive' response
"""
@app.route('/ping/<new_node_id>')
def ping(new_node_id):
    remote_ip = request.remote_addr
    print remote_ip
    node.update_node_list({new_node_id:remote_ip})
        
    return jsonify(node_id=node.node_id)


@app.route('/search/<filename>')
def search(filename):
    global nodes
    with open(filename) as fd:
        return fd.read()
    return "nok"    


def search_for_file(filename):
    urls = [node[filename] for node in nodes]
    for url in urls:
        requests.get(url + "/search/" + filename)


@app.route('/store/<filename>')
def store(filename, methods=['PUT']):
    f = request.files['the_file']
    f.save(filename)

@app.route('/dist-store/<filename>')
def dist_store(filename, methods=['PUT']):
    global nodes
    urls = [node['score'] for node in nodes]
    requests.put(urls[0] + "/store/" + filename, data=request.files['the_file'])


def store_file(filename):
    edge_url = None
    with open(filename, "rb") as fd:
        requests.put(edge_url + "/store/" + filename, data=fd.read())


def start_edge(edge_url=None):
    node = None
    try:
        port = 5000
        if edge_url:
            node = Node(edge_url, node_id="03ffae4vaf")
            port += 1
        else: # master
            node = Node()
        
        app.run(host='0.0.0.0', debug=True, port=port)
        return node
    except:
        return False
    
