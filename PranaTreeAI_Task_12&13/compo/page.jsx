import React from 'react'

export default function page() {

    let socket = new webSocket("ws://localhoost:8000");

    socket.onopen = function(event){
      displayMessage("connected to the webstocket server.","server")
    }

    socket.onmessage = function (event){
      displayMessage(event.data,"server")
    }


    const sendMessage = () =>{
       let message = document.getElementById("messageInput").value;
      if (message.trim() !== "") {
      
      socket.send(message);
      displayMessage(message, "client"); 
  
      document.getElementById("messageInput").value = ""; 
      }
    }
   })

  return (
    <div>
      <h1>Web sockets</h1>

      <div className='chat_box'> 

      </div>
      
      <input type="text" className='input_box' placeholder='type here' id='messageInput' />
      <button onClick={}>Send</button>
    </div>
  )

