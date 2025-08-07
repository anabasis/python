import socket

def run_client(host='127.0.0.1', port=7788):
    with socket.socket() as sock:
        sock.connect((host, port))
        for _ in range(10):
            data = input(">>")
            sock.sendall(data.encode())
            if data == 'bye':
                sock.close()
                break
            res = sock.recv(1024)
            print(res.decode())

if __name__ == '__main__':
    print("multi client start")
    run_client()
    print("multi client end")
