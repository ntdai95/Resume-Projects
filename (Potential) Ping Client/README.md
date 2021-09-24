**Ping Client:**

*How to run:*
The ping client will accept the server_ip, server_port (integer between 1024 and 65535 inclusive), count (integer greater than 0), period (float greater than 0), timeout (float greater than 0) values in this order.

For example, please run the client as shown below:<br/>
python ping_client.py &lt; server_ip &gt; &lt; server_port &gt; &lt; count &gt; &lt; period &gt; &lt; timeout &gt;

1. Initiate the ping client by entering the ping server's ip address, port number, the total number of total ping requests that you would like to make (count), the amount of time to wait between sending each ping request to the server (period), and the amount of time to wait for a reply from the ping server for each ping request (timeout).
2. The Ping client will parse out the user input arguments and validate them. If it's correct then, it will start runing the program; otherwise, it will send back a warning message.
3. It will create a new thread for each ping request and does not discard any thread to be able to print out the complete statistics at the end.
4. For each ping request, it will create a checksum packet and put it inside of the data packet in network byte order (big endian) and send it to the server through a socket. Then, it will wait until the reply for the request comes back or the timeout happens before sending the next request.
5. To detect errors, it calculates the checksum (ones' complement of the ones' complement sum) of each received request.
6. If there is no server present, then it will still sends out all of the requests, but since all of them will timeout, it will printout the statistics of no reply received.
