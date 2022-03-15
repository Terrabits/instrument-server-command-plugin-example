from socket import socket


# constants
SERVER_ADDRESS = ('localhost', 9000)

# connect
client = socket()
client.connect(SERVER_ADDRESS)

# get id_string
client.sendall(b'is_rs_devices?\n')
result = client.recv(1024)
print(f'is_rs_devices? {result.strip().decode()}')
