import socket
import time

class UdpSpeedTester:
    def __init__(self, src_address, dst_address):
        self.download_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.download_socket.bind((src_address[0], int(src_address[1])))
        self.dst_address = dst_address
        self.upload_socket = None
        self.max_testing_time = 10.00
        self.packet_size = 1024


    def run_upload_test(self):
        pass
      

    def run_download_test(self):
        pass        
       

    def run(self, execution_type):
        if execution_type == "-df":
            self.run_download_test()
            self.run_upload_test()
        else:
            self.run_upload_test()
            self.run_download_test()
