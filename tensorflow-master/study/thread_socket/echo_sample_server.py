'''simple echo server'''
import socket

def run_server(host='127.0.0.1', port=7788):
    BUF_SIZE = 1024
    with socket.socket() as sock:
        sock.bind((host, port))
        sock.listen()
        conn, addr = sock.accept()
        while True:
            data = conn.recv(BUF_SIZE)
            msg = data.decode()
            print(data.decode())
            conn.sendall(data)
            if msg == 'bye':
                conn.close()
                break

if __name__ == '__main__':
    print("server sample start")
    run_server()
    print("server sample end")
