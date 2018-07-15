import nidaqmx
from drawnow import *
from matplotlib.widgets import Button, Cursor
import matplotlib.animation as animation
import daqplot
import random
import peakdetect
import matplotlib.pyplot as plt
from math import *
import os
from numpy import *

samples = 60
samplesPerSecond = 1000
voltage0 = []
voltage1 = []
timeval = []
value = True
anim = []
count = 0
bpval = []
fig, ax1, readbutton, stopbutton = [], [], [], []


def randomgen():
    vol00,vol11 = [], []
    for i in range(samples):
        vol00.append(sin(2*pi*500*i/8000.0)*cos(2*pi*100*i/8000.0))
        vol11.append(2*cos(2*pi*400*i/8000.0)*3*cos(2*pi*50*i/8000.0))
    return [vol00,vol11]


def readChannel(channel):
    try:
        with nidaqmx.Task() as task:
            task.ai_channels.add_ai_voltage_chan(channel)
            task.timing.cfg_samp_clk_timing(rate=samplesPerSecond, samps_per_chan=samples)
            return task.read(number_of_samples_per_channel=samples, timeout=25.0)
    except:
        return randomgen()



def timegenerate():
    global count, timeval
    times = []
    if count == 0 or count == 1:
        t = 0
    else:
        t = timeval[len(timeval) - 1]
    for i in range(samples):
        times.append(t)
        t += 1.0/samples
    return times


def bclose(event):
    plt.close(1)


def makefig(i):
    global count,fig
    try:
        result = readChannel('Dev1/ai0:1')
        vol0, vol1 = result[0], result[1]
        tim = timegenerate()
        if count > 0:
            for x in range(samples):
                voltage0.append(vol0[x])
                voltage1.append(vol1[x])
                timeval.append(tim[x])
            plotgraph()
            plt.pause(0.000001)

            for i in range(int(samples*0.55)):
                voltage0.pop(0)
                voltage1.pop(0)
                timeval.pop(0)
        count += 1
    except:
        raise


def returnvalue(event):
    global voltage0, voltage1, timeval, bpval
    _pause()
    bpval = daqplot.process(voltage0, voltage1, timeval)


def plotgraph():
    global ax1, readbutton, stopbutton
    ax1.clear()
    plt.subplot(2, 1, 1)
    plt.plot(timeval, voltage0, 'r-', label='voltage0')
    plt.legend(loc='upper right')
    plt.subplot(2, 1, 2)
    plt.plot(timeval, voltage1, 'b-', label='voltage1')
    plt.legend(loc='upper right')
    readaxis = fig.add_axes((0.5, 0.005, 0.1, 0.05))
    readbutton = Button(readaxis, 'Read', hovercolor='1.0')
    readbutton.on_clicked(returnvalue)
    stopaxis = fig.add_axes((0.75, 0.005, 0.1, 0.05))
    stopbutton = Button(stopaxis, 'Stop', hovercolor='1.0')
    stopbutton.on_clicked(bclose)


def _pause():
    global anim
    anim.event_source.stop()


def main():
    global anim, fig, ax1
    fig = plt.figure()
    ax1 = fig
    anim = animation.FuncAnimation(fig, makefig, interval=1)
    # show plot
    try:
        plt.show()
    except :
        pass
    finally:
        plt.close()


def sendval():
    global bpval
    return bpval


def filelog(tab,text,no,mode):
    flog = open('timelog.csv', mode)
    flog.write('%s%d,%s\n'%('Waveform', no, 'Values'))
    flog.write('%s,%s\n' % ('Time', text))
    for i in range(len(tab)):
        flog.write('%f,%f\n'%(tab[i][0],tab[i][1]))
    flog.close()


def peak():
    global voltage0, voltage1, timeval
    maxtab0, mintab0 = peakdetect.peakdet(voltage0, 0.1, timeval) # change 2nd argument to fine tune peak detection
    maxtab1, mintab1 = peakdetect.peakdet(voltage1, 0.1, timeval) # change 2nd argument to fine tune peak detection
    filelog(maxtab0,'Maximum',1,'w')
    filelog(mintab0, 'Minimum', 1, 'a')
    filelog(maxtab1, 'Maximum', 2, 'a')
    filelog(mintab1, 'Minimum', 2, 'a')
    plt.subplot(2,1,1)
    plt.plot(timeval,voltage0)
    plt.scatter(array(maxtab0)[:, 0], array(maxtab0)[:, 1], color='blue')
    plt.scatter(array(mintab0)[:, 0], array(mintab0)[:, 1], color='red')
    plt.subplot(2,1,2)
    plt.plot(timeval, voltage1)
    plt.scatter(array(maxtab1)[:, 0], array(maxtab1)[:, 1], color='blue')
    plt.scatter(array(mintab1)[:, 0], array(mintab1)[:, 1], color='red')
    os.startfile('timelog.csv')
    plt.show()

if __name__ == '__main__':
    print readChannel('Dev1/ai0:1')
