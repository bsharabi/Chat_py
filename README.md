# Chat_py
Version py 3.9.7
## Description:
* This is an implementation of Selective Repeat reliable transport layer protocol.
![alt](https://upload.wikimedia.org/wikipedia/commons/b/bb/Client-Server_3-tier_architecture_-_en.png)
![alt](https://www.researchgate.net/profile/Paris-Avgeriou/publication/215835792/figure/fig11/AS:339719922700300@1458006949899/3-tier-client-server-architecture-example.png)

## TCP protocol
* To better understand this, check out the sequence of socket API calls and data flow for TCP:
  
![alt](https://files.realpython.com/media/sockets-tcp-flow.1da426797e37.jpg)

## UDP protocol
* To better understand this, check out the sequence of socket API calls and data flow for UDP:
  
![alt](https://media.geeksforgeeks.org/wp-content/uploads/UDP.png)


## Selective Repeat ARQ
* Selective Repeat ARQ is also known as the Selective Repeat Automatic Repeat Request. It is a data link layer protocol that uses a sliding window method. The Go-back-N ARQ protocol works well if it has fewer errors. But if there is a lot of error in the frame, lots of bandwidth loss in sending the frames again. So, we use the Selective Repeat ARQ protocol. In this protocol, the size of the sender window is always equal to the size of the receiver window. The size of the sliding window is always greater than 1.

* If the receiver receives a corrupt frame, it does not directly discard it. It sends a negative acknowledgment to the sender. The sender sends that frame again as soon as on the receiving negative acknowledgment. There is no waiting for any time-out to send that frame. The design of the Selective Repeat ARQ protocol is shown below.

![alt](https://static.javatpoint.com/tutorial/computer-network/images/sliding-window-protocol-3.png)
* The example of the Selective Repeat ARQ protocol is shown below in the figure.
![alt](https://static.javatpoint.com/tutorial/computer-network/images/sliding-window-protocol-4.png)


## UML

## Running Server:
```bash
# Clone the repository
$ git clone https://github.com/bsharabi/Chat_py.git
# Go into the repository
$ cd Server
# Open the terminal on Windows
$ Run "python3.9 Controller <host> <port>"
# Open the terminal on Linux
$ Run "python3 Controller <host> <port>"
# Example
$ Run "python3/3.9 Controller localhost 3000"
```

## Running Client:
```bash
# Clone the repository
$ git clone https://github.com/bsharabi/Chat_py.git
# Go into the repository
$ cd Client
# Open the terminal on Windows
$ Run "python3.9 Controller.py"
# Open the terminal on Linux
$ Run "python3 Controller"
```

## How To Run App:
```bash
# Clone the repository
$ git clone https://github.com/bsharabi/Chat_py.git
# Go into the repository
* first:
  You must first run the server (use the steps above)
-----------------------------------------------------
* Second:
  you need to run the client (use the steps above)
  Note that the choice of host and port is the same between the two parties
```

