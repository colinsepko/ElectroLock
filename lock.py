import bluetooth
import RPi.GPIO as GPIO
import time

# GPIO setup
GPIO.setmode(GPIO.BCM)
LOCK_PIN = 18  # Replace with the GPIO pin connected to the lock mechanism
GPIO.setup(LOCK_PIN, GPIO.OUT)

# Initialize the lock in the "locked" state
GPIO.output(LOCK_PIN, GPIO.HIGH)

def lock():
    print("Locking...")
    GPIO.output(LOCK_PIN, GPIO.HIGH)
    time.sleep(1)  # Simulate lock activation time
    print("Locked.")

def unlock():
    print("Unlocking...")
    GPIO.output(LOCK_PIN, GPIO.LOW)
    time.sleep(1)  # Simulate unlock activation time
    print("Unlocked.")

# Bluetooth server setup
server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
server_sock.bind(("", bluetooth.PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]
print(f"Waiting for a connection on RFCOMM channel {port}...")

# Advertise the service
bluetooth.advertise_service(server_sock, "LockControlServer",
                            service_classes=[bluetooth.SERIAL_PORT_CLASS],
                            profiles=[bluetooth.SERIAL_PORT_PROFILE])

try:
    client_sock, client_info = server_sock.accept()
    print(f"Accepted connection from {client_info}")

    while True:
        # Receive data from the app
        data = client_sock.recv(1024).decode('utf-8').strip()
        if not data:
            break

        print(f"Received command: {data}")
        # Handle lock/unlock commands
        if data.lower() == "lock":
            lock()
            client_sock.send("Locked.\n")
        elif data.lower() == "unlock":
            unlock()
            client_sock.send("Unlocked.\n")
        elif data.lower() == "exit":
            print("Exiting...")
            client_sock.send("Goodbye.\n")
            break
        else:
            client_sock.send("Unknown command. Use 'lock', 'unlock', or 'exit'.\n")

except KeyboardInterrupt:
    print("Server shutting down...")

except Exception as e:
    print(f"Error: {e}")

finally:
    # Clean up
    GPIO.cleanup()
    server_sock.close()
    print("Server closed.")
