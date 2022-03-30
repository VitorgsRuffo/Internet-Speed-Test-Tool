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
execution_mode = sys.argv[5]

from SpeedTester import SpeedTester

# main
tester = SpeedTester((src_ip, int(src_port)), (dst_ip, int(dst_port)), execution_mode)
tester.run()
