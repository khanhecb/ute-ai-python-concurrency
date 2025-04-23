#!/bin/python
# Date: 23/4/2025
# Author: KhanhECB
# Link: https://execnet.readthedocs.io/en/latest/example/hybridpython.html
# Mô tả: Giao tiếp giữa Python 3 và Python 2.7 bằng execnet. 

import execnet
gw = execnet.makegateway("popen//python=python2.7")
channel = gw.remote_exec("""
    import numpy
    array = numpy.array([1,2,3])
    while 1:
        x = channel.receive()
        if x is None:
            break
        array = numpy.append(array, x)
    channel.send(repr(array))
""")
for x in range(10):
    channel.send(x)
channel.send(None)
print (channel.receive())

# env: ai_env
# Run: python2.7 main.py
# Result
# array([1, 2, 3, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9])