"use client"
import React, { useState } from "react";
import { TextField, Button, List, ListItem, ListItemText, Avatar, Box } from "@mui/material";

const ChatUI = () => {
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState("");

  const handleSend = () => {
    if (newMessage.trim()) {
      setMessages([...messages, { text: newMessage, sender: "User" }]);
      setNewMessage(""); // Clear input field
    }
  };

  return (
    <Box
      sx={{
        display: "flex",
        flexDirection: "column",
        height: "400px",
        width: "300px",
        border: "1px solid #ccc",
        borderRadius: "8px",
        padding: "16px",
        marginLeft:"30%",
        marginTop:"100px"
      }}
    >
      {/* Messages List */}
      <List sx={{ flexGrow: 1, overflowY: "auto" }}>
        {messages.map((msg, index) => (
          <ListItem key={index}>
            <Avatar sx={{ marginRight: "8px" }}>{msg.sender[0]}</Avatar>
            <ListItemText primary={msg.text} secondary={msg.sender} />
          </ListItem>
        ))}
      </List>

      {/* Input Box */}
      <Box sx={{ display: "flex", alignItems: "center" }}>
        <TextField
          value={newMessage}
          onChange={(e) => setNewMessage(e.target.value)}
          variant="outlined"
          size="small"
          fullWidth
          placeholder="Type a message"
        />
        <Button onClick={handleSend} variant="contained" sx={{ marginLeft: "8px" }}>
          Send
        </Button>
      </Box>
    </Box>
  );
};

export default ChatUI;
