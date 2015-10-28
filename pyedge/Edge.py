import requests

class Node():
    
    def __init__(self):
        self.node_id = None #this will be generated later?
        self.node_list = []
        self.bucket_size = 5

    def _ping(self, node_id):
        return self._rpc("ping", node_id)


    def ping(self, node_id):
        if self._ping(node_id):
            self.node_list = []

    def store(self, data):
        pass

    def find_node(self):
        pass

    def find(self, data_id):
        pass

    def _update_bucket_list(self, node_id):
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
                        
        
    def _rpc(self, call, **kwargs):
        try:
            if call == "ping":
                node_url = kwargs[0]
                result = requests.get(node_url)
                if result.ok:
                    return True
        except:
            print "error in rpc"
        
