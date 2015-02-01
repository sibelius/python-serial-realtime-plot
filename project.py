import re
import serial
import matplotlib.pyplot as plt
import time
import sys
from sqlalchemy import Column, Integer, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from collections import deque

engine = create_engine('sqlite:///data.db')
Base = declarative_base()

class Data(Base):
    __tablename__ = 'data'

    _id = Column(Integer, primary_key=True, autoincrement=True)
    client = Column(Integer)
    source = Column(Integer)
    value1 = Column(Float)
    value2 = Column(Float)
    status = Column(Integer)

    def __repr__(self):
        return "<Data(client=%d, source=%d, value1=%f, value2=%f, status=%d>" % \
                (self.client, self.source, self.value1, self.value2, self.status)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

#tripa = 'c00000000001i00000000001t22.22222p33.33333s00001e.'

def parse_data(tripa):
    """Parse a string from the serial port
    >>> parse_data('c00000000001i00000000001t22.22222p33.33333s00001e.')
    (1, 1, 22.22222, 33.33333, 1)
    """
    _, client, source, value1, value2, status, _ = re.split('c|i|t|p|s|e', tripa)
    client = int(client)
    source = int(source)
    value1 = float(value1)
    value2 = float(value2)
    status = int(status)

    return client, source, value1, value2, status

def save_data(Session, client, source, value1, value2, status):
    """Save the data to the sqlite database"""
    data = Data(client=client, source=source, value1=value1, value2=value2, status=status)
    print(data)

    session = Session()
    session.add(data)
    session.commit()

v1 = deque([0]*100)
v2 = deque([0]*100)
#ax = plt.axes(xlim=(0, 20), ylim=(0, 10))
plt.subplot(211)
plt.ylim([0,100])
plt.ion()
line1, = plt.plot(v1)
plt.show(block=False)

plt.subplot(212)
plt.ion()
plt.ylim([0,100])
line2,  = plt.plot(v2)
plt.show(block=False)

def plot_data(value1, value2):
    plt.subplot(211)
    plt.title('%f' % value1)
    v1.appendleft(value1)
    datatoplot = v1.pop()
    line1.set_ydata(v1)

    plt.subplot(212)
    plt.title('%f' % value2)
    v2.appendleft(value2)
    datatoplot = v2.pop()
    line2.set_ydata(v2)

    plt.draw()
    plt.pause(0.0001)

def main(port):
    ser = serial.Serial(port)
    while True:
        tripa = ser.readline()
        print(tripa)
        client, source, value1, value2, status = parse_data(tripa.decode('utf-8'))
        save_data(Session, client, source, value1, value2, status)
        plot_data(value1, value2)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        port = '/dev/ttys005'
    else:
        port = sys.argv[1]

    main(port)
