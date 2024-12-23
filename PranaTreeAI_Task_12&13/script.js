
const webSocket = require("ws")
const wss = new webSocket.Server({port:8080})

wss.on("connection",ws =>{
 console.log(`new client connected , total no of clients: ${wss.clients.size}`);

 ws.send(`Welcome to the websocket server`);

 ws.on('message',(message) =>{
     console.log(`Recived from client: ${message}`);
     ws.send(`server response: you sent ->${message}`);
 });

 setInterval(() =>{
     ws.send('Totaly there are'+wss.clients.size+'clients connected  to the sever')
 },50000);
 ws.on('close', () => console.log(`client disconnectd , total no of client: ${wss.clients.size}`))
});

console.log('websocket running on ws://localhost:8080')