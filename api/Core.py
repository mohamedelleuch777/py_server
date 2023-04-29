import sys
import json

input_object = ""
data_retrieved = False

# "METHOD": "GET",
# "DATA": params,
# "PATH": self.path,
# "HOST": self.headers.get('Host'),
# "DIRECTORY": self.root


def ReadReqData():
    global input_object, data_retrieved
    if not data_retrieved:
        input_json = sys.stdin.read()
        input_object = json.loads(input_json)
        data_retrieved = True


def ReadReqMethod():
    ReadReqData()
    return input_object['METHOD']


def ReadReqParams():
    ReadReqData()
    return input_object['DATA']


def ReadReqPath():
    ReadReqData()
    return input_object['PATH']


def ReadReqHost():
    ReadReqData()
    return input_object['HOST']


def ReadReqDirectory():
    ReadReqData()
    return input_object['DIRECTORY']
