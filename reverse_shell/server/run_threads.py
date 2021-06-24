import socket
import threading 
import time
from queue import Queue
import sys

import server

PORT=9990
HOST=""
MAX_BAD_CONNECTIONS=5
NUMBER_OF_THREADS=2
TASKS=[1,2] 

queue=Queue()


def create_worker_threads():
	for _ in range(NUMBER_OF_THREADS):
		t=threading.Thread(target=worker)
		t.daemon=True
		t.start()



def worker():
	while True:
		task_ID=queue.get()
		if task_ID==1:
			server.create_socket()
			server.bind_socket()
			server.accept_client_connection()
		elif task_ID==2:
			server.start_myShell()

		queue.task_done()



def create_jobs():
	for task_ID in TASKS:
		queue.put(task_ID)

	queue.join()



def main():
	create_worker_threads()
	while True:
		create_jobs()



if __name__=="__main__":
	main()
