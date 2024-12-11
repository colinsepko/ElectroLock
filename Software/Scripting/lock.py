import bluetooth
import RPi.GPIO as GPIO
import time
import subprocess

# GPIO setup
GPIO.setmode(GPIO.BCM)
LOCK_PIN = 18  # Replace with the GPIO pin connected to the lock mechanism
GPIO.setup(LOCK_PIN, GPIO.OUT)

# Initialize the lock in the "locked" state
GPIO.output(LOCK_PIN, GPIO.HIGH)

def lock():
    """Engage the lock."""
    print("Locking...")
    GPIO.output(LOCK_PIN, GPIO.HIGH)
    time.sleep(1)  # Simulate lock activation time
    print("Locked.")

def unlock():
    """Disengage the lock."""
    print("Unlocking...")
    GPIO.output(LOCK_PIN, GPIO.LOW)
    time.sleep(1)  # Simulate unlock activation time
    print("Unlocked.")

def make_discoverable():
    """Enable discoverable and pairable mode on the Raspberry Pi."""
    subprocess.run(["bluetoothctl", "power", "on"], check=True)
    subprocess.run(["bluetoothctl", "discoverable", "on"], check=True)
    subprocess.run(["bluetoothctl", "pairable", "on"], check=True)
    print("Raspberry Pi is now discoverable and pairable.")


CHARACTERISTIC_UUID = "0000abcd-0000-1000-8000-00805f9b34fb"
def start_bluetooth_server():
    """Set up the Bluetooth server and handle connections."""
    server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    server_sock.bind(("", bluetooth.PORT_ANY))
    server_sock.listen(1)

    port = server_sock.getsockname()[1]
    print(f"Advertising service on RFCOMM channel {port}...")

    bluetooth.advertise_service(
        server_sock,
        "LockControlServer",
        service_id=CHARACTERISTIC_UUID,
        service_classes=[bluetooth.SERIAL_PORT_CLASS],
        profiles=[bluetooth.SERIAL_PORT_PROFILE],
    )

    print("Waiting for a connection...")
    client_sock, client_info = server_sock.accept()
    print(f"Accepted connection from {client_info}")

    try:
        while True:
            # Receive data from the client
            data = client_sock.recv(1024).decode("utf-8").strip()
            if not data:
                break

            print(f"Received command: {data}")
            # Handle lock/unlock commands
            if data.lower() == "lock":
                lock()
                client_sock.send(b"Locked.\n")
            elif data.lower() == "unlock":
                unlock()
                client_sock.send(b"Unlocked.\n")
            elif data.lower() == "exit":
                print("Exiting...")
                client_sock.send(b"Goodbye.\n")
                break
            else:
                client_sock.send(b"Unknown command. Use 'lock', 'unlock', or 'exit'.\n")
    except Exception as e:
        print(f"Connection error: {e}")
    finally:
        client_sock.close()
        server_sock.close()
        print("Bluetooth server closed.")

if __name__ == "__main__":
    try:
        make_discoverable()
        start_bluetooth_server()
    except KeyboardInterrupt:
        print("Shutting down...")
        subprocess.run(["bluetoothctl", "discoverable", "off"], check=True)
        subprocess.run(["bluetoothctl", "pairable", "off"], check=True)
    finally:
        GPIO.cleanup()
        print("GPIO cleaned up.")
