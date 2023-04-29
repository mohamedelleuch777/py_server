from server import MyServer
from http.server import HTTPServer
import constant

hostName = constant.HOST
serverPort = constant.PORT

#from files import Files
#f = Files()
#cntnt = f.Read("server.py")
#print(cntnt)


def LaunchServer():
    MyServer.webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))
    try:
        MyServer.webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    MyServer.webServer.server_close()
    print("Server stopped.")


if __name__ == '__main__':
    LaunchServer()
