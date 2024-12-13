Raspberry Pi OS design and customization

The Raspberry Pi was installed with the normal Raspberry Pi OS distribution, described as a port of Debian Bookworm. The version with an included desktop was downloaded, however the minimal version that does not include a desktop is recommended in the future due to the complete neglect of the desktop functionality during development. After the initial download was complete, a few components remained to be installed.

1. RPi Connect
Software developed by the organization behind the Raspberry Pi itself for remotely accessing a terminal shell within the pi. SSH was incredibly ineffective for accessing the pi for unknown reasons, and RPi Connect seemed to work much better for similarly unkown reasons.
2. PyBluez
A Python library allowing bluetooth socket listening and communication through Python.

Primary Contributor: Colin Sepkovic
