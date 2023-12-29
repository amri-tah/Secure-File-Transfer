# Secure File Transfer System with Merkle Tree

This repository contains a secure file transfer system implemented in Python, providing a reliable and encrypted method for uploading, downloading, and displaying files between a client and server. The system incorporates Fernet symmetric encryption for secure data transmission and uses Merkle trees for integrity verification.


![app](https://github.com/amri-tah/Secure-File-Transfer/assets/111682039/0d246345-3d0f-4ce6-b4ee-d69bd3a58d1b)


## Features

- **Secure Communication:**
  - Utilizes sockets for reliable communication between the client and server.
  - Implements Fernet symmetric encryption to secure file data during transmission.

- **Merkle Tree Integrity Verification:**
  - Breaks files into chunks and constructs a Merkle tree to verify data integrity.
  - Ensures files are transferred without corruption or loss.

- **User-Friendly Interface with Streamlit:**
  - A Streamlit web application provides an intuitive interface for users.
  - Supports file upload, download, and file listing functionalities.

- **Logging and Error Handling:**
  - Implements logging for better traceability and debugging.
  - Error handling to manage unexpected scenarios.

## Repository Structure

- **client.py:** Client-side implementation, including functions for file upload, download, and displaying available files.
  
- **server.py:** Server-side implementation, managing client connections, handling file transfers, and implementing Merkle tree verification.

- **logs.csv:** Log file storing important events, timestamps, and the status of file transfers.

- **requirements.txt:** Lists necessary dependencies for running the system.

## How to Use

1. Clone the repository to your local machine.
   ```bash
   git clone https://github.com/amri-tah/Secure-File-Transfer.git
   ```

2. Install the required dependencies.
   ```bash
   pip install -r requirements.txt
   ```

3. Run the server script on the server.
   ```bash
   python server.py
   ```

4. Open the Streamlit web application on the client side.
   ```bash
   python client.py
   ```

Interact with the system through the web interface to securely upload, download, and display files.

## Screenshots

#### Show Files in Server:

![no-files](https://github.com/amri-tah/Secure-File-Transfer/assets/126688534/15184999-0a52-4a02-a0e7-4035588c9265)
![show-files](https://github.com/amri-tah/Secure-File-Transfer/assets/126688534/7f24d14e-9290-45cc-9615-1095c3a201bd)


#### Upload Files to Server:

![upload](https://github.com/amri-tah/Secure-File-Transfer/assets/126688534/8a68204a-a015-432c-a0dc-5c46bdbb14b6)

#### Download Files from Server:
![download](https://github.com/amri-tah/Secure-File-Transfer/assets/126688534/09c03509-4f0d-4679-b7b8-e7bede9f2ea6)
![download-no-file](https://github.com/amri-tah/Secure-File-Transfer/assets/126688534/4d92e36b-7b48-440b-974c-0fffbbf00842)

