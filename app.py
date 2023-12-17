from hashlib import sha256
import socket
import streamlit as st

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
    root_hash = list(tree.keys())[-1]
    return root_hash

def upload_file(filename, ip):
    IP = socket.gethostbyname(socket.gethostname())
    PORT = 4455
    ADDR = (IP, PORT)
    FORMAT = 'utf-8'
    SIZE = 1024

    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(ADDR)
    except:
        st.error("Connection Failure! Check if the server is active.")
        return

    file = open(filename, 'r')
    data = file.read()
    client.send(filename.encode())
    msg = client.recv(SIZE).decode(FORMAT)
    print(f"Server: {msg}")
    client.sendall(data.encode(FORMAT))
    ch = chunk_file(filename, 1024)
    hash1 = merkle_tree(ch)
    print(f"Hash value: {hash1}")
    client.sendall(hash1.encode(FORMAT))

    secure = client.recv(SIZE).decode(FORMAT)
    if secure == "True":
        st.success("Data Integrity assured!")
    else:
        st.error("Data might be lost.")
    
    msg = client.recv(SIZE).decode(FORMAT)
    print(f"Server: {msg}")
    file.close()
    client.close()
    if msg == "File data recieved":
        return True
    return False

def download_file(filename, ip):
    IP = socket.gethostbyname(socket.gethostname())
    PORT = 4455
    ADDR = (IP, PORT)
    FORMAT = 'utf-8'
    SIZE = 1024

    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(ADDR)
    except:
        st.error("Connection Failure! Check if the server is active.")
        return

    file = open(filename, 'r')
    data = file.read()
    client.send(filename.encode())
    msg = client.recv(SIZE).decode(FORMAT)
    print(f"Server: {msg}")
    client.sendall(data.encode(FORMAT))
    ch = chunk_file(filename, 1024)
    hash1 = merkle_tree(ch)
    print(f"Hash value: {hash1}")
    client.sendall(hash1.encode(FORMAT))

    msg = client.recv(SIZE).decode(FORMAT)
    print(f"Server: {msg}")
    file.close()
    client.close()

    if msg == "File data recieved":
        return True
    return False

if __name__ == "__main__":
    st.title("Secure File Transfer System using Merkle Tree")
    st.subheader("Verify in a Flash ⚡")
    st.write("Develop a secure file transfer system that utilizes a Merkle tree to ensure file integrity during transmission. The system should encrypt the file upon upload to the server and employ the Merkle tree to verify the file's authenticity upon download.")
    ip = st.text_input("Enter IP address of the server: ")
    uploaded_file = st.file_uploader("Choose a text file!", accept_multiple_files=True)
    upload = st.button("Upload Files!")
    if upload:
        if uploaded_file:
            filenames = []
            for x in uploaded_file:
                if upload_file(x.name, ip):
                    st.success(f'File {x.name} was transferred successfully!', icon="✅")
                    filenames.append(x.name)
                else:
                    st.error(f'There is some problem with transferring {x.name}! Try again', icon="🚨")
            print(filenames)
        else:
            st.error(f'Browse files to upload first!', icon="🚨")

    filename = st.text_input("Enter file you want to download from the server: ")
    download = st.button("Download File")
    
    if download:
        if filename:
            if download_file(filename, ip):
                st.success(f'File {filename} was downloaded successfully!', icon="✅")
            else:
                st.error(f'No such file {filename} exists on the server! Try again', icon="🚨")

        else:
            st.error(f'Enter a filename to be downloaded first!', icon="🚨")




