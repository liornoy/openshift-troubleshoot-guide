import socket
import time
import argparse

# Define target host, port, packet size, and delay
HOST = "127.0.0.1"  # Replace with target server IP
PORT = 8080  # Replace with target server port
PACKET_SIZE = 1500
DELAY = 0.001  # 1 millisecond

def sender():
  # Create a TCP socket
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  # Connect to the server
  sock.connect((HOST, PORT))

  # Infinite loop for sending data
  while True:
    # Create data packet
    data = b"A" * PACKET_SIZE  # Fill packet with "A" characters

    # Send data
    sock.sendall(data)

    # Introduce delay between sends
    time.sleep(DELAY)

  # Close the socket (would never be reached in infinite loop)
  sock.close()

def receiver():
  # Create a TCP socket
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  # Bind the socket to the address and port
  sock.bind((HOST, PORT))

  # Listen for incoming connections
  sock.listen()

  # Accept a connection
  conn, addr = sock.accept()

  # Infinite loop for receiving data
  while True:
    # Receive data (reads 1 byte at a time)
    data = conn.recv(1)

    # Check if connection is closed
    if not data:
      break

    # Introduce delay between reads (optional for simulating slow processing)
    time.sleep(DELAY)  # Uncomment for optional delay

  # Close the connection
  conn.close()

  # Close the socket
  sock.close()

  print("Connection closed")

# Define command-line arguments
parser = argparse.ArgumentParser(description="TCP Stress Test Script (Sender or Receiver)")
parser.add_argument("mode", choices=["sender", "receiver"], help="Choose mode (sender or receiver)")
args = parser.parse_args()

# Run the chosen function based on the argument
if args.mode == "sender":
  sender()
elif args.mode == "receiver":
  receiver()
else:
  print("Invalid mode. Please choose 'sender' or 'receiver'.")
