import os
import socket
from hashlib import sha256

IP = socket.gethostbyname(socket.gethostname())
PORT = 4455
ADDR = (IP,PORT)
FORMAT = 'utf-8'
SIZE = 1024

def chunk_file(file_path, chunk_size):
    chunks = []
    with open(file_path, "rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if chunk:
                chunks.append(chunk)
            else:
                break
    return chunks

def hash_chunk(chunk):
    return sha256(chunk).hexdigest()

def merkle_tree(chunks):
    tree = {}
    leaves = []
    for chunk in chunks:
        leaf_hash = hash_chunk(chunk)
        leaves.append(leaf_hash)
        tree[leaf_hash] = None

    while len(leaves) > 1:
        new_leaves = []
        for i in range(0, len(leaves), 2):
            left = leaves[i]
            right = leaves[i + 1] if i + 1 < len(leaves) else None
            parent_hash = sha256(left.encode() + (right.encode() if right else b"")).hexdigest()
            tree[parent_hash] = [left, right]
            new_leaves.append(parent_hash)
        leaves = new_leaves
    root_hash = list(tree.keys())
    return root_hash[-1]


def main():
    print("Server is starting...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print("Server is listening")
    

    while True:
        conn,  addr = server.accept()
        print(F"New connection {addr} connected.")
        transfertype = conn.recv(SIZE).decode(FORMAT)
        if transfertype=="Upload":
            filename = conn.recv(SIZE).decode(FORMAT)
            print(f"Filename: {filename} received")
            file = open("Recieved data/"+ filename, 'w')
            conn.send("filename recieved".encode(FORMAT))

            data = conn.recv(SIZE).decode(FORMAT)
            hash_val = conn.recv(SIZE).decode(FORMAT)
            print(f"Hash value {hash_val}")

            ch = chunk_file(filename, 1024)
            hash2 = merkle_tree(ch)
            print(f"Hash value: {hash2}")

            if hash2 == hash_val:
                conn.send("True".encode(FORMAT))
                print('Your data is in good hands')
            else:
                conn.send("False".encode(FORMAT))
                print('Your data is not in good hands')

            print(f"File Data Recieved")
            file.write(data)
            conn.send("File data recieved".encode(FORMAT))
            file.close()

        elif transfertype=="Download":
            filename = conn.recv(SIZE).decode(FORMAT)
            print(f"Filename: {filename} received")
            if os.path.exists("Recieved data/" + filename):
                conn.send("Exist".encode(FORMAT))
                file = open("Recieved data/"+ filename, 'r')
                data = file.read()
                conn.send(data.encode())
                file.close()

                ch = chunk_file("Recieved data/"+filename, 1024)
                hash1 = merkle_tree(ch)
                print(f"Hash value: {hash1}")
                conn.send(hash1.encode(FORMAT))
            else:
                conn.send("Not exist".encode(FORMAT))
        conn.close()

        print(f"Disconnected {addr} ")

if __name__ == '__main__':
    main()