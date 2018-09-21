#!/usr/bin/env python3
import sys, socket, json, pickle, hashlib, os
from optparse import OptionParser
from watson_developer_cloud import TextToSpeechV1
from BridgeKeys import watson_api_key, watson_url
from cryptography.fernet import Fernet
from lib import print_checkpoint

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
    if os.path.exists("speech.wav"):
        os.remove("speech.wav")

'''
with open('hello_world.wav', 'wb') as audio_file:
    audio_file.write(
        tts_service.synthesize(
            'Hello world', 'audio/wav', 'en-GB_KateVoice').get_result().content)
voices = tts_service.list_voices().get_result()
print(json.dumps(voices, indent=2))
'''    
def create_payload(crypt_key, text, md5_hash):
    payload_dict = {}
    if len(crypt_key) > 0:
        payload_dict['crypt_key'] = key
    payload_dict['text'] = text
    payload_dict['md5_hash'] = md5_hash
    pickle_bytes = pickle.dumps(payload_dict)
    return pickle_bytes

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

        chk_msg = 'Created socket at 0.0.0.0 on port ' + str(server_port)
        print_checkpoint(chk_msg)

        try:
            listener.bind(('', bridge_port))
            listener.listen(backlog_size)
        except Exception as err:
            print(err)
            listener.close()

        chk_msg = 'Listening for client connections\n'
        print_checkpoint(chk_msg)

        try:
            chk_msg = 'Connecting to ' + server_ip + ' on port ' + server_port
            print_checkpoint(chk_msg)
            sender.connect((server_ip, server_port))
            #test = 'What is the meaning of life?'
            #key = Fernet.generate_key()
            #f = Fernet(key)
            #test = f.encrypt(b"what is the meaning of life")
            #print("encrypted the text")
            #m = hashlib.md5()
            #m.update(test)
            #print("created md5Hash")
            #pickled = create_payload(key, test, m.hexdigest())
            #test = pickle.dumps(pickled)
            #sender.send(pickled)
            #answer = sender.recv(socket_size)
        except Exception as err:
            print(err)
            sender.close()

        client, address = listener.accept()
        chk_msg = 'Accepted client connection from ' + str(address) + ' on port ' + str(bridge_port)
        print_checkpoint(chk_msg)

        
        while 1:
            data = client.recv(socket_size)
            
            if data:
                
                data = pickle.loads(data)
                chk_msg = 'Received data ' + str(data)
                print_checkpoint(chk_msg)

                
                m = hashlib.md5()

                if data['crypt_key']:
                    key = data['crypt_key']
                    f = Fernet(key)
                    text = data['text']
                    
                    md5_hash = data['md5_hash']
                    m.update(text)

                    text_str = f.decrypt(text)
                    chk_msg = 'Decrypt: Key: ' + key.decode() + ' | Plaintext \n ' + text_str.decode()
                    print_checkpoint(chk_msg)
                    #token = f.encrypt(str.encode(text_str)
                
                    if m.hexdigest() == md5_hash:
                        chk_msg = 'Speaking Question: ' + text.decode() + '\n'
                        print_checkpoint(chk_msg)
                        textToSpeech(text_str.decode())            
                        pickle_bytes = create_payload(key, text, m.hexdigest())

                        try:
                            chk_msg = 'Sending data ' + pickle_bytes.decode() + '\n'
                            print_checkpoint(chk_msg)
                            sender.send(pickle_bytes)
                            answer = sender.recv(socket_size)
                            chk_msg = 'Received data ' + answer.decode()
                        except:
                            client.close()
                        answerLoads = pickle.loads(answer)
                        answ_text = answerLoads['text']
                        answ_md5_hash = answerLoads['md5_hash']
                        m1 = hashlib.md5()

                        m1.update(answ_text)

                        if m1.hexdigest() == answ_md5_hash:

                            answ_str = f.decrypt(answ_text)
                            chk_msg = 'Decrypt: Using Key: ' + key.decode() + ' | Plaintext: ' + answ_text.decode()
                            print_checkpoint(chk_msg)

                            chk_msg = 'Speaking Answer: ' + answ_str.decode()
                            print_checkpoint(chk_msg)
                            textToSpeech(answ_str.decode())
                            
                            answ_pickle = create_payload('', answ_text, answ_md5_hash)
                            client.send(answ_pickle)
                        else:
                            print("incorrect checksum")
                    else:
                        print("incorrect checksum")
            



