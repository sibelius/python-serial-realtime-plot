# python-serial-realtime-plot

Realtime plotting of data from serial plot

## First install the requirements
pip install -r requirements.txt

## Usage - virtual serial port

## Create the virtual serial port
./virtualserial.sh

2015/02/01 15:08:43 socat[45262] N PTY is /dev/ttys008 (read)

2015/02/01 15:08:43 socat[45262] N PTY is /dev/ttys009 (write)

2015/02/01 15:08:43 socat[45262] N starting data transfer loop with FDs [3,3] and [5,5]

## Run project python to generate the realtime charts
python project.py /dev/ttys008

## Simulate the tripa for the serial port
./simulate.sh /dev/ttys009
