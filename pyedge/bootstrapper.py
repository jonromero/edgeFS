from flask import Flask, request
import requests
app = Flask(__name__)

edgeNodes = {'127.0.0.1:5000': 99,
             '127.0.0.1:8000': 93}

edgeIndex = [{'README.txt': [{'ip': '127.0.0.1:5000',
                              'ip': '127.0.0.1:5001'}]},
              {'.gitignore': [{'ip': '32.233.44.56:8000'}]}
                               
             ]

@app.route('/')
def hello_world():
    return 'Hello World!', edgeIndex, edgeNodes


@app.route('/connect/<url>')
def connect(url):
    global edgeNodes
    remote_ip = request.remote_addr
    # if new connection
    if remote_ip not in edgeNodes.keys():
        edgeNodes[remote_ip] = 50
    return edgeNodes

def connect_to_edge(host):
    global edgeIndex
    response = requests.get(host + "/connect/" + "127.0.0.1:5000")
    edgeIndex = response.json()



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

        
if __name__ == '__main__':
    app.run(debug=True)
    
