import sys

argvlen = len(sys.argv)
if argvlen < 6:
    print("Error: invalid execution format.\nFormat: pythonX main.py src_ip src_port dst_ip dst_port (-df | -uf)")
    quit(1)

# getting execution arguments...
src_ip = sys.argv[1]
src_port = sys.argv[2]
dst_ip = sys.argv[3]
dst_port = sys.argv[4]
execution_type = sys.argv[5]

# classes
class SpeedTester:
    def __init__(self, ip: str, port: int):
        self.tcp_speed_tester = TcpSpeedTester()
        self.udp_speed_tester = UdpSpeedTester()


    def run(self):
        self.tcp_speed_tester.


# main
print("\n\nWelcome to VW internet speed test tool!\n")
tester = SpeedTester(src_ip, src_port)
tester.run()
