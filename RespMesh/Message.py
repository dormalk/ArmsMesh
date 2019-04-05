import time
class Message:

    def __init__(self):
        self.dest = None
        self.src = None
        self.time = time.time()
        self.data = ''
        self.msg_id = None

    def get_message(self):
        if self.dest is not None:
            msg = 'd:' + str(self.dest) + '\n'
        if self.data is not None:
            msg += 'm:' + self.data + '\n'
        if self.time is not None:
            msg += 't:' + str(self.time) + '\n'
        return msg
    
    def set_time(self,time):
        self.time=time

    def get_time(self):
        return self.time

    def set_dest(self,nodeid):
        self.dest = nodeid

    def get_dest(self):
        return self.dest

    def set_data(self,data):
        self.data = data
    
    def get_data(self):
        return self.data

    def set_src(self,src):
        self.src = src
    
    def get_src(self):
        return self.src

    def set_msg_id(self,msg_id):
        self.msg_id = msg_id
    
    def get_msg_id(self):
        return self.msg_id
