CPU load and network connection monitoring
==========================================

Simply logs cpu load and open network connections to sqlite database inside while true.
Tested on ubuntu 16.04. Not robust.

# Requirements

 * Python 3
 * Python virtualenv
 * *nix

# Install

```
cp config.file.example config.file
virtualenv -p /usr/bin/python3 venv
source venv/bin/activate
pip install -r requirements.txt
./monitor.py db-create
```

# Starting the monitor

```
./monitor.py start
```

The network connections monitoring requires root privileges and the monitor
should be runningas background process. Starting the monitor in screen:

```
screen -S monitord
sudo su
./monitor.py start
#  Ctrl-A + Ctrl-D
```
