import requests
import uuid

class Node():
    
    def __init__(self, node_id=None, edge_url):
        self.node_id = node_id if node_id else uuid.getnode()
        self.node_list = []
        self.bucket_size = 5

        if not self.ping_and_update(edge_url):
            raise "%s edge node cannot be found"

    def _ping(self, edge_url):
        return self.__rpc("ping", url=edge_url)
    
    def ping_and_update(self, node_id):
        if self._ping(node_id):
            self.node_list = [node_id]

    def store(self, data):
        pass

    def find_node(self):
        pass

    def find(self, data_id):
        pass

    def update_node_list(self, node_id):
        # node exists, put it in the back
        if node_id in self.node_list:
            self.node_list.remove(node_id)
            self.node_list.append(node_id)
            
        # node doesn't exist and bucket is full
        elif len(self.node_list) > self.bucket_size:
            # ping all nodes
            for stored_node_id in self.node_list:
                # this node was not found, so remove it and add the new node
                # if all nodes are still active, don't use the new node 
                if not self._ping(stored_node_id):
                    self.node_list.remove(stored_node_id)
                    self.node_list.append(node_id)
                    
        # node doesn't exist and bucket isn't full
        else:
            self.node_list.append(node_id)
                        
        
    def __rpc(self, call, **kwargs):
        try:
            if call == "pong":
                node_url = kwargs[0]
                result = requests.get(node_url)
                if result.ok:
                    return True
        except:
            print "error in rpc"
        
