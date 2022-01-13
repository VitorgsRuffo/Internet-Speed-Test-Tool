import socket
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

        self.upload_socket.send("ok".encode()) #synchronization...
        self.upload_socket.recv(1024) 

        start_time = time.time()
        print("\nTesting upload...")
        while (time.time() - start_time) < self.max_testing_time:
            self.upload_socket.send(buffer)
            self.upload_socket.recv(1024)
            packets_sent += 1
        
        self.upload_socket.shutdown(socket.SHUT_RDWR)
        self.upload_socket.close()
        self.upload_socket = None

        test_time = round(time.time() - start_time, 2)
        print("Upload finished!")
        print("\nTest report:")
        print("------------")
        print(f"\tbits/s: {round(((self.packet_size * packets_sent * 8) / test_time) / 1024, 2)}K")
        print(f"\tpackets/s: {round(packets_sent / test_time, 2)}")
        print(f"\ttotal bytes transferred: {(self.packet_size * packets_sent)/1024}K")
        print(f"\ttest time: {test_time} seg")
        print(f"\tlost packets: 0")


    def run_download_test(self):
        
        connection, addr = self.download_socket.accept()
        packets_received = 0
        
        connection.recv(1024) #synchronization...
        connection.send("ok".encode())

        start_time = time.time()
        print("\nTesting download...")
        while True:
            bytes_read = connection.recv(self.packet_size)
            if not bytes_read:
                break
            connection.send("ok".encode())
            packets_received += 1
        
        connection.shutdown(socket.SHUT_RD)
        connection.close()

        test_time = round(time.time() - start_time, 2)
        print("Download finished!")
        print("\nTest report:")
        print("------------")
        print(f"\tbits/s: {round(((self.packet_size * packets_received * 8) / test_time) / 1024, 2)}K")
        print(f"\tpackets/s: {round(packets_received / test_time, 2)}")
        print(f"\ttotal bytes transferred: {(self.packet_size * packets_received)/1024}K")
        print(f"\ttest time: {test_time} seg")
        print(f"\tlost packets: 0")


    def run(self, execution_type):
        if execution_type == "-df":
            self.run_download_test()
            self.run_upload_test()
        else:
            self.run_upload_test()
            self.run_download_test()
