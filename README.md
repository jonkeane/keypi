This was an experiment to turn a Raspberry Pi into a Human Interface Device (HID). A keyboard to be more precise.

Generally based off of https://gist.github.com/ukBaz/a47e71e7b87fbc851b27cde7d1c0fcf0 which is based off of http://yetanotherpointlesstechblog.blogspot.com/2016/04/emulating-bluetooth-keyboard-with.html

I wanted to move to Python3 and tidy things up on the Bluetooth side to bring it in to line with current ways things are done in BlueZ.

## Configure Raspberry Pi.
These instructions assuming you have BlueZ 5.43 installed. You can check this with:
```
$ bluetoothctl -v
5.43
```

Ensure Raspberry Pi is at the latest version:
```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get dist-upgrade
```

Check that the packages required for this are installed, might also need `python3-gi` (or `pygobject3` on macos)
```
sudo apt-get install python3-dbus
```

On macos, might need to manually (only if there are errors about gi module not found):

```
brew install pygobject3
PKG_CONFIG_PATH=/usr/local/opt/libffi/lib/pkgconfig ARCHFLAGS="-arch x86_64" pip install pygobject
```

## Installation, testing
Create an env:
```
python3 -m venv keypi
source keypi/bin/activate
```

Install dependencies
```
(keypi) $ pip install -r requirements.txt
(keypi) $ pip install -r requirements-test.txt
(keypi) $ pip install -e .
```

```
(keypi) $ pytest -vv keypi
```

## Reconfigure the Bluetooth Daemon
The instructions worked that were provided but things have moved on a little bit. To stop the Bluetooth daemon running then the following command is preferred:
```
sudo service bluetooth stop
```

The `input` and `battery` Bluetooth plugins need to be removed so that it does not grab the sockets we require access to. As the original author says the way this was documented could be improved. If you want to restart the daemon (without the input plugin) from the command line then the following would seem the preferred:
```
sudo /usr/lib/bluetooth/bluetoothd --noplugin=input,battery
```

If you want to make this the default for this Raspberry Pi then modify the `/lib/systemd/system/bluetooth.service` file. You will need to change the Service line from:
```
ExecStart=/usr/lib/bluetooth/bluetoothd
```
to
```
ExecStart=/usr/lib/bluetooth/bluetoothd --compat --noplugin=input,battery
```

## Configure D-Bus
When a new service is created on the D-Bus, this service needs to be configured.
```
sudo cp com.jonkeane.keypiservice.conf /etc/dbus-1/system.d
```

## Install at a system level
```
pip install -e .
sudo pip install -e .
```

## Pairing

### Terminal 1

TODO: change this into a systemctl service

```
pi@raspberrypi:~/keypi $ sudo keypi server start
Setting up service
Setting up BT device
Configuring for name KeyPi_Keyboard
Configuring Bluez Profile
Reading service record
Profile registered
Waiting for connections
 ```
Scan for the keyboard Pi and connect from main computer
```
8C:2D:AA:44:0E:3A connected on the control socket
8C:2D:AA:44:0E:3A connected on the interrupt channel
```

### Terminal 2
```
pi@raspberrypi:~/keypi $ keypi input open
pi@raspberrypi:~/keypi $ keypi input close
pi@raspberrypi:~/keypi $ keypi input custom
```

### Terminal 3

Only needed for the first time pairing, to accept the code and agree:

```
pi@raspberrypi:~/keypi $ sudo bluetoothctl
```