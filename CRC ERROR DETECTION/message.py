class Message:
    def __init__(self,send_matrix,crc_code):
        self.send_matrix=send_matrix
        self.crc_code=crc_code
    
    def empty(self):
        self.send_matrix=[]
        self.crc_code=b''