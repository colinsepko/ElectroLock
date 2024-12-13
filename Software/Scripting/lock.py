import RPi.GPIO as GPIO
import time
import keyboard  # Install this with 'pip install keyboard'

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

if __name__ == "__main__":
    try:
        is_locked = True  # Start with the lock engaged
        print("Press the space bar to toggle the lock state.")
        print("Press Ctrl+C to exit.")

        while True:
            # Detect if the space bar is pressed
            if keyboard.is_pressed("space"):
                if is_locked:
                    unlock()
                    is_locked = False
                else:
                    lock()
                    is_locked = True

                # Wait for the key to be released to avoid multiple toggles
                while keyboard.is_pressed("space"):
                    time.sleep(0.1)

    except KeyboardInterrupt:
        print("Shutting down...")
    finally:
        GPIO.cleanup()
        print("GPIO cleaned up.")
