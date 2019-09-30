import socket
import sys
import random
import os
from ctypes import *

class STATUS(Structure):
    _pack_ = 1
    _fields_ = [("code",c_int)]

class Customer(Structure):
    _pack_ = 1
    _fields_ = [("id", c_int),
                ("name", c_char*100),
                ("age", c_int)
                ]
class Data(Structure):
    _pack_ = 1
    _fields_ =[("method",c_int), ("customer",Customer), ("status",STATUS) ]

def main():
    server_addr = ('localhost', 38110)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.connect(server_addr)
        print("Connected to %s" % repr(server_addr))
    except:
        print("ERROR: Connection to %s refused" % repr(server_addr))
        sys.exit(1)

    try:
        while True:
            option = raw_input('Create or read customer?(C/r)')
            if option in ['C']:
                id = int(raw_input("ID (0-99):"))
                if id not in range(0,100):
                    print('Interval 1 through 100!')
                    break
                name = raw_input('Name:')
                age = int(raw_input('Age:'))
                customer_input = Customer(id=id,name=name, age=age) 

                print("Sending id=%d, name=%s,  age=%d"  % (customer_input.id,
                                                customer_input.name,
                                                customer_input.age
                                                ))
                data = Data(customer = customer_input, method=1, status=STATUS(code=0))

            else:
                id = int(raw_input("Input the customer's ID: "))
                customer_input = Customer(id=id,name = 'None', age = 0) 
                data = Data(customer = customer_input, method=2, status=STATUS(code=0))
            
            nsent = s.send(data)
            print("Sent %d bytes" % nsent)
            buff = s.recv(sizeof(Data))
            data_output = Data.from_buffer_copy(buff)
            print("\n\nMessage from server")
            print('Status code: %d ' % data_output.status.code)
            if data_output.status.code == 200:
                print("SUCCESS!")
            elif data_output.status.code == 500:
                print("ERROR!")
            elif data_output.status.code == 404:
                print("NOT FOUND!")
            if data_output.customer.id != -1:
                print('ID: %d' % data_output.customer.id)
                print('Name: %s' % data_output.customer.name)
                print('Age: %d' % data_output.customer.age)
            
            option = raw_input('Do you wish to continue?(y/N)')
            if option not in ['y']:
                break
            else:
                os.system('clear')

    finally:
        print("Closing socket")
        s.close()


if __name__ == "__main__":
    main()
