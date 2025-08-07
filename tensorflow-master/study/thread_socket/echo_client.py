## '''echo_client.py'''
import socket

def run(host='127.0.0.1', port=4000):
    print("client run")
    with socket.socket() as s:
        s.connect((host, port))
        line = input('>')
        s.sendall(line.encode())
        resp = s.recv(1024)
        print(f'={resp.decode()}')

if __name__ == '__main__':
    print("clinet send")
    run()
    print("clinet end")
