#!/bin/python
# Date: 23/4/2025
# Author: KhanhECB
# Description: Dumping and loading values across interpreter versions
# Link: https://execnet.readthedocs.io/en/latest/example/hybridpython.html


import execnet
def execnet_example_dump_load():
    """
    Execnet hổ trợ tuần tự và giải tuần tự các đối tượng Python.
    Điều này an toàn hơn sử dụng pickle.
    """
 
    # Write dump data Python2
    with open("data.py23", "wb") as f:
        f.write(execnet.dumps(["hello", "world"]))

    # Read dump data - Python3
    with open("data.py23", "rb") as f:
        val = execnet.loads(f.read(), py2str_as_py3str=True)
    assert val == ["hello", "world"]
