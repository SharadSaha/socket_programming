from prompt_toolkit import prompt,HTML
from prompt_toolkit import print_formatted_text as print
from prompt_toolkit.styles import Style

import socket
import threading 
import time
from queue import Queue
import sys,os,signal

import server

PORT=9990
HOST=""
MAX_BAD_CONNECTIONS=5
NUMBER_OF_THREADS=2


style = Style.from_dict({
    'aaa': '#ff0066',
    'bbb': '#44ff00',
    'yyy': '#ffff00'
})



def shell_decoration():
	print(HTML('<aaa>\t\t----------------------------</aaa>'),style=style)
	print(HTML('<bbb>\n\n\t\t|| WELCOME TO CUSTOM SHELL ||</bbb>'),style=style)
	print(HTML('<bbb>\t\tEnter lst for list of commands..\n\n</bbb>'),style=style)
	print(HTML('<aaa>\t\t----------------------------</aaa>'),style=style)



#List all currently active connections
def list_of_connections():
	results=''
	BUFFER_SIZE=999999

	for ID,connection in enumerate(server.connections):
		try: #Check whether connection is active
			testing_data=str.encode("test")
			connection.send(testing_data)
			connection.recv(BUFFER_SIZE)
		except:
			del server.connections[ID]
			del server.addresses[ID]
			continue

		results=str(ID)+".   "+str(server.addresses[ID][0])+ "   "+str(server.addresses[ID][1])+"\n"

	if not results:
		results="     NO ACTIVE CLIENTS\n\n"

	print(HTML('<yyy>\n\n|----------CLIENTS----------|\n</yyy>'+results),style=style)




def display_list_of_commands():
	print(HTML("<yyy>\tYou can type in the following commands : </yyy>"),style=style)
	print(HTML("<yyy>\t1. clients : displays the currently active clients</yyy>"),style=style)
	print(HTML("<yyy>\t2. choose : type 'choose' followed by client ID to start connection</yyy>"),style=style)
	print(HTML("<yyy>\t3. exit : to exit myShell</yyy>"),style=style)



#Creating custom shell
def start_myShell():
	time.sleep(0.05)
	shell_decoration()
	time.sleep(0.01)

	while True:

		shell_command=prompt(HTML('<aaa>myshell></aaa>'),style=style)


		if shell_command=="clients":
			list_of_connections()

		elif "choose" in shell_command:
			new_connection=server.get_client(shell_command)
			if new_connection:
				server.send_commands(new_connection)

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

