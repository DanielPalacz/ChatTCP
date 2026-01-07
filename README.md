# ChatTCP
Simple Chat TCP

### Tech-details
```
recv - buffer - \n
    * recv() → transport
    * buffer → protocol
    * \n → application contract

```

### Manual tests:
```
 - Close client by Ctrl+C
 - Execute 'kill -9'
 - Send message and close socket immediately.

```

### Client with 's.shutdown(socket.SHUT_WR)'
```
It means:
 - I will be not sending, but I am still receiving.
 - Client uses correct "half-close" flow. Server can't crash.

From TCP point of view:
 - Client sends FIN
 - Server received: recv() → b''
 - but Server still can send data (to Client)
 - no RST or  BrokenPipe

No ConnectionResetError/BrokenPipeError. Everything ends in normal way (happy path).
Due to 's.shutdown(socket.SHUT_WR)' some nasty flows cant be achieved.
```

### Evil clients
```
1. ConnectionResetError (RST)
This code:
   import os
   os._exit(0)

will cause:
   no FIN
   kernel sends RST
   Server: ConnectionResetError


2. BrokenPipeError
This code in Client:
    s.sendall(b"hello\n")
    s.close()

and in Server side:
    sendall() after a while (or in next recv-loop)

will cause:
    Server will write to closed socket => BrokenPipeError.


3. Leave data in buffer and disappear

Client:
    s.sendall(b"incomplete message")
    s.close()
Server:
    recv will receive data
    next recv() → b''
    buffer doesnt have '\n'
 
 * Hereby, architectural question: what to do with incomplete message?

```