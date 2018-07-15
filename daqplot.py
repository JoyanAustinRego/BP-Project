def bpmap(diff):
    in_min = 0.0
    in_max = 5.0
    out_max = 80
    out_min = 140
    return (diff - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def process(voltage0, voltage1, timeval):
    tmax0 = timeval[voltage0.index(min(voltage0))]
    tmax1 = timeval[voltage1.index(min(voltage1))]
    diff = max(tmax0,tmax1) - min(tmax0, tmax1)
    return bpmap(diff)

if __name__ == '__main__':
    print process([i for i in range(10)],[i for i in range(10)],[i for i in range(10)])

