Lock design

A solenoid lock is used as the lock to be controlled by the pi. Rather than the pi conditionally supplying power to the lock, a power relay is used instead. The pi supplies power to the relay, and a GPIO pin (18 specifically) controls whether the power relay completes the circuit that the lock is on or not. The lock is powered by a 12V battery.

Primary contributor: Joseph Lee

