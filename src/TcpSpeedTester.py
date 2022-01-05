import socket
import os
import time

class TcpSpeedTester:

    def __init__(self, src_address, dst_address):
        self.download_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.download_socket.bind((src_address[0], int(src_address[1])))
        self.download_socket.listen(100)
        self.dst_address = dst_address
        self.upload_socket = None
        self.max_testing_time = 10.00
        self.packet_size = 1024


    def run_upload_test(self):

        self.upload_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.upload_socket.connect((self.dst_address[0], int(self.dst_address[1])))
        buffer = bytes(self.packet_size)
        packets_sent = 0

        #self.upload_socket.send("ok".encode()) #synchronization...
        start_time = time.time()
        
        print("Testing upload...")
        while (time.time() - start_time) < self.max_testing_time:
            bytes_s = self.upload_socket.send(buffer)
            packets_sent += 1
            #print(f"packet {packets_sent} - {time.time()-start_time} - {bytes_s}...")

        test_time = round(time.time() - start_time, 2)
        print("Upload test finished!")
        print("Test report:")
        print(f"bits/s: {round((self.packet_size * packets_sent * 8) / test_time, 2)}")
        print(f"packets/s: {round(packets_sent / test_time, 2)}")
        print(f"total bytes transferred: {self.packet_size * packets_sent}")
        print(f"test time: {test_time}")
        print(f"lost packets: 0")

        self.upload_socket.shutdown(socket.SHUT_RDWR)
        self.upload_socket.close()
        self.upload_socket = None


    def run_download_test(self):
        
        connection, addr = self.download_socket.accept()
        packets_received = 0
        
        #connection.recv(1024) #synchronization...
        start_time = time.time()

        print("Testing download...")
        bytes_read = connection.recv(self.packet_size)
        while bytes_read:
            packets_received += 1
            #print(f"packet {packets_received}...")
            bytes_read = connection.recv(self.packet_size)

        test_time = round(time.time() - start_time, 2)
        print("Download test finished!")
        print("Test report:")
        print(f"bits/s: {round((self.packet_size * packets_received * 8) / test_time, 2)}")
        print(f"packets/s: {round(packets_received / test_time, 2)}")
        print(f"total bytes transferred: {self.packet_size * packets_received}")
        print(f"test time: {test_time}")
        print(f"lost packets: 0")

        connection.shutdown(socket.SHUT_RD)
        connection.close()


    def run(self, execution_type):
        if execution_type == "-df":
            self.run_download_test()
            #sync...
            self.run_upload_test()
        else:
            self.run_upload_test()
            #sync...
            self.run_download_test()
