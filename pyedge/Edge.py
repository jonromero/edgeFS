import requests
import uuid

class Node():
    
    def __init__(self, edge_url, node_id=None):
        self.node_id = node_id if node_id else uuid.getnode()
        self.node_list = []
        self.bucket_size = 5

        if not self.ping_and_update(edge_url):
            raise "%s edge node cannot be found"

    def _ping(self, edge_url):
        return self.__rpc("ping", url=edge_url)
    
    def ping_and_update(self, node_url):
        node_id  = self._ping(node_url)
        if node_id:
            self.node_list = [{node_id:node_url}]
            return True
        else:
            return False
        
    def store(self, data):
        pass

    def find_node(self):
        pass

    def find(self, data_id):
        pass

    def update_node_list(self, node):
        node_id = node.keys()[0]
        # node exists, put it in the back
        if node_id in self.node_list.keys():
            self.node_list.remove(node)
            self.node_list.append(node)
            
        # node doesn't exist and bucket is full
        elif len(self.node_list) > self.bucket_size:
            # ping all nodes
            for stored_node in self.node_list:
                # this node was not found, so remove it and add the new node
                # if all nodes are still active, don't use the new node
                stored_node_url = stored_node.values()[0]
                if not self._ping(stored_node_url):
                    self.node_list.remove(stored_node)
                    self.node_list.append(node)
                    
        # node doesn't exist and bucket isn't full
        else:
            self.node_list.append(node)
                        
        
    def __rpc(self, call, **kwargs):
        try:
            if call == "ping":
                node_url = kwargs[0]
                result = requests.get(node_url+"/ping/"+self.node_id)
                return result.json()['node_id']
        except:
            print "error in rpc"
        
