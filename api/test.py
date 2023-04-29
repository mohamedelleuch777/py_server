from Core import *

response = (f"\n"
            f"<h1>serving python files works</h1>\n"
            f"<p>\n"
            f"Method is: {ReadReqMethod()} <br>\n"
            f"Data: {ReadReqParams()}\n"
            f"</p>\n")

print(response)
