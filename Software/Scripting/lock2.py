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

def get_connected_device():
    """Check for connected Bluetooth devices using bluetoothctl."""
    try:
        result = subprocess.run(
            ["bluetoothctl", "paired-devices"],
            stdout=subprocess.PIPE,
            text=True,
            check=True
        )
        devices = result.stdout.strip().split("\n")
        for device in devices:
            if "electrolock" in device:  # Replace 'electrolock' with your app's device name
                return device.split(" ")[1]  # Return the MAC address
        return None
    except Exception as e:
        print(f"Error checking connected devices: {e}")
        return None

def listen_for_commands():
    """Start listening for commands from a paired Bluetooth device."""
    device_address = get_connected_device()
    if not device_address:
        print("No connected device found. Ensure your app is paired and connected.")
        return

    print(f"Connected to {device_address}. Listening for commands...")

    # Create a Bluetooth socket for communication
    try:
        server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        server_sock.bind((device_address, bluetooth.PORT_ANY))
        server_sock.listen(1)

        client_sock, client_info = server_sock.accept()
        print(f"Connection established with {client_info}")

        while True:
            data = client_sock.recv(1024).decode("utf-8").strip()
            if not data:
                break
            print(f"Received command: {data}")
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
        print(f"Bluetooth error: {e}")
    finally:
        server_sock.close()
        GPIO.cleanup()
        print("Socket closed and GPIO cleaned up.")

if __name__ == "__main__":
    try:
        while True:
            listen_for_commands()
            time.sleep(1)  # Check connection status periodically
    except KeyboardInterrupt:
        print("Shutting down...")
    finally:
        GPIO.cleanup()
        print("GPIO cleaned up.")
