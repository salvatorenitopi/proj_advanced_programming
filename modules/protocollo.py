import base64
import custom_crypt as ce

KEY = "crypto-key"

def b64_encode (string):
    return base64.encodestring (string)

def b64_decode (string):
    return base64.decodestring (string)

def recvall(sock, n):
    data = ''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data

def send(sock, msg):
    msg = ce.encrypt( b64_encode (msg), KEY )

    l = str(len(msg))
    for i in range (0, 10 - len(str(len(msg)))):
        l = "0" + l

    frame = l + msg 
    sock.sendall(frame)


def recv(sock):
    raw_msglen = recvall(sock, 10)

    if not raw_msglen:
        return None

    msglen = int(raw_msglen[0:10])
    return b64_decode( ce.decrypt( recvall(sock, msglen), KEY ))


