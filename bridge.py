#!/usr/bin/env python3
import sys, socket, json
from optparse import OptionParser
from watson_developer_cloud import TextToSpeechV1
from BridgeKeys import watson_username, watson_password


tts_service = TextToSpeechV1(
    username = watson_username,
    password = watson_password)
#with open('hello_world.wav', 'wb') as audio_file:
 #   audio_file.write(
  #      tts_service.synthesize(
   #         'Hello world', 'audio/wav', 'en-US_AllisonVoice').get_result().content)
voices = tts_service.list_voices().get_result()
print(json.dumps(voices, indent=2))
    

"""
def parse_args(args):
    parser = OptionParser()
    parser.add_option("--svr-p", dest="server_port", help="server port", metavar="SVRPORT")
    parser.add_option("--svr", dest="server_ip", help="server IP", metavar="IP")
    parser.add_option("-p", dest="bridge_port", help="bridge port", metavar="PORT")
    parser.add_option("-b", dest="backlog_size", help="backlog size", metavar="SIZE")
    parser.add_option("-z", dest="socket_size", help="socket size", metavar="SIZE")

    return parser.parse_args()

if __name__ == "__main__":
    opts, args = parse_args(sys.argv[1])
    print(opts)
    server_port = int(opts.server_port)
    server_ip = opts.server_ip
    bridge_port = int(opts.bridge_port)
    backlog_size = int(opts.backlog_size)
    socket_size = int(opts.socket_size)

    try:
        sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as msg:
        print('Failed to create sockets. Error code: ' + str(msg[0]) + ', ' + msg[1])
        sys.exit();
    sender.connect((server_ip, server_port))
    listener.bind((socket.gethostname(), bridge_port))
    listener.listen(backlog_size)                   
    while 1:
        client, address = listener.accept()
        data = conn.recv(socket_size)
        if data:
            client.send(data)
        client.close()


"""
