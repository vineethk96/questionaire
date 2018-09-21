#!/usr/bin/env python3
import sys, socket, json, pickle, hashlib, os
from optparse import OptionParser
from watson_developer_cloud import TextToSpeechV1
from BridgeKeys import watson_api_key, watson_url
from cryptography.fernet import Fernet

tts_service = TextToSpeechV1(
    iam_apikey = watson_api_key,
    url = watson_url)

def textToSpeech(text):
    print("in the function")
    with open('speech.wav', 'wb') as audio_file:
        print("opening file")
        audio_file.write(
            tts_service.synthesize(
                text, 'audio/wav', 'en-GB_KateVoice').get_result().content)
    os.system('aplay speech.wav')
    print("deleting")
    #if os.path.exists("speech.wav"):
        #os.remove("speech.wav")

'''
with open('hello_world.wav', 'wb') as audio_file:
    audio_file.write(
        tts_service.synthesize(
            'Hello world', 'audio/wav', 'en-GB_KateVoice').get_result().content)
voices = tts_service.list_voices().get_result()
print(json.dumps(voices, indent=2))
'''    


def parse_args(args):
    parser = OptionParser()
    parser.add_option("--svr-p", dest="server_port", help="server port", metavar="SVRPORT")
    parser.add_option("--svr", dest="server_ip", help="server IP", metavar="IP")
    parser.add_option("-p", dest="bridge_port", help="bridge port", metavar="PORT")
    parser.add_option("-b", dest="backlog_size", help="backlog size", metavar="SIZE")
    parser.add_option("-z", dest="socket_size", help="socket size", metavar="SIZE")

    return parser.parse_args()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        textToSpeech('hello world')
        
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
       # sender.connect((server_ip, server_port))
        listener.bind(('', bridge_port))
        listener.listen(backlog_size)
        client, address = listener.accept()

        while 1:
            data = client.recv(socket_size)
            if data:
                data = pickle.loads(data)
                print(str(data))
                textToSpeech(data)
                m = hashlib.md5()
                
        #        sender.send(data)
                if data['crypt_key']:
                    key = data['crypt_key']
                    text = data['text']
                    md5_hash = data['md5_hash']
                    text = f.decrypt(text)
                    token = f.encrypt(text)
                    m.update(token)
                    if m.hexdigest() == md5_hash:
                        textToSpeech(text)            
            
                        payload_dict = {}
                        payload_dict['crypt_key'] = key
                        payload_dict['text'] = token
                        payload_dict['md5_hash'] = m.hexdigest()
                        pickle_bytes = pickle.dumps(payload_dict)

                        #sender.send(pickle_bytes)
                        #answer = sender.recv(socket_size)

                        #answerLoads = pickle.loads(answer)
                        #answ_text = answerLoads['text']
                        #answ_md5_hash = answerLoads['md5_hash']
                        #m1 = hashlib.md5()
                        #m1.update(answ_text)
                        '''if m1.hexdigest() == answ_md5_hash:
                            answ_str = f.decrypt(answ_text)
                            textToSpeech(answ_str)
                            answ_payload = {}
                            answ_payload['text'] = answ_text
                            answ_payload['md5_hash'] = answ_md5_hash
                            answ_pickle = pickle.dumps(answ_payload)
                            client.send(answ_pickle)
                        else:
                            print("incorrect checksum")
                    else:
                        print("incorrect checksum")
            '''



