import socket
import os
import time

class TcpSpeedTester:

    def __init__(self, src_address, dst_address):
        self.download_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.download_socket.bind((src_address[0], src_address[1]))
        self.download_socket.listen(100)
        self.upload_socket = None
        self.max_testing_time = 10.00


    def run_upload_test(self):

        self.upload_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.upload_socket.connect((self.dst_address[0], self.dst_address[1]))
        packet_size = 1024
        buffer = bytes(packet_size)
        packets_sent = 0
        start_time = time.time()

        print("Testing upload...")
        while (time.time() - start_time) < self.max_testing_time:
            self.upload_socket.send(buffer)
            packets_sent += 1

        test_time = round(time.time() - start_time, 2)
        print("Upload test finished!")
        print("Test report:")
        print(f"bits/s: {round((packet_size * packets_sent * 8) / test_time, 2)}")
        print(f"packets/s: {round(packets_sent / test_time, 2)}")
        print(f"total bytes transferred: {packet_size * packets_sent}")
        print(f"test time: {test_time}")
        print(f"lost packets: 0")


    def run_download_test(self):
        pass


    def run(self, execution_type):
        if execution_type == "-df":
            self.run_download_test()
            #sync...
            self.run_upload_test()
        else:
            self.run_upload_test()
            #sync...
            self.run_download_test()
