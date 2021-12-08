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

Check that the packages required for this are installed
```
sudo apt-get install python3-dbus
```

Here is an outline of things I changed:
## Moved to Python3
I wanted to do this because not only is it a good thing to do but it also allowed some of the dependancies to be removed. After Python 3.3 Bluetooth sockets are supported in the native Python installs. The downside to this is that there are clear distinctions between str and bytes in the code. For me, this broke the keyboard client. This is what required the biggest re-write to get Python3 working.

## Reconfigure the Bluetooth Daemon
The instructions worked that were provided but things have moved on a little bit. To stop the Bluetooth daemon running then the following command is preferred:
```
sudo service bluetooth stop
```

The `input` Bluetooth plugin needs to be removed so that it does not grab the sockets we require access to. As the original author says the way this was documented could be improved. If you want to restart the daemon (without the input plugin) from the command line then the following would seem the preferred:
```
sudo /usr/lib/bluetooth/bluetoothd -P input
```

If you want to make this the default for this Raspberry Pi then modify the `/lib/systemd/system/bluetooth.service` file. You will need to change the Service line from:
```
ExecStart=/usr/lib/bluetooth/bluetoothd
```
to
```
ExecStart=/usr/lib/bluetooth/bluetoothd -P input
```

## Configure D-Bus
When a new service is created on the D-Bus, this service needs to be configured.
```
sudo cp com.jonkeane.btkkbservice.conf /etc/dbus-1/system.d
```

## Pairing

### Terminal 1

TODO: change this into a systemctl service

```
pi@raspberrypi:~/keypi $ sudo /usr/libexec/bluetooth/bluetoothd --compat --noplugin=input,battery
```

### Terminal 2
```
pi@raspberrypi:~/keypi $ sudo service bluetooth stop
pi@raspberrypi:~/keypi $ sudo /usr/lib/bluetooth/bluetoothd -P input &
pi@raspberrypi:~/keypi $ sudo python3 keypi_server.py
Setting up service
Setting up BT device
Configuring for name BT_HID_Keyboard
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

### Terminal 3
```
pi@raspberrypi:~/keypi $ python3 keypi_client.py
```

### Terminal 4

Only needed for the first time pairing, to accept the code and agree:

```
pi@raspberrypi:~/keypi $ sudo bluetoothctl
```