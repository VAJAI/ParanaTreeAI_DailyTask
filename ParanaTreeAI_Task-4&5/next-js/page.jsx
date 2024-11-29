"use client";
import React, { useEffect, useRef, useState } from "react";
import Navebar from './components/Navebar'

export default function page() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState([]);
  const [loading, setLoading] = useState(false);

  const chatContainerRef = useRef(null);

  const handlesubmit = async (e) => {
    if (!question.trim()) return;
    e.preventDefault();
    setLoading(true);
    setAnswer((prev) => [...prev, { question, answer: "..." }]);
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/ask`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text: question }),
      });
      if (!response.ok) {
        throw new Error("Failed to Fetch response");
      }
      const data = await response.json();
      console.log(data);
      const answer = data.Answer || "no response recived";

      setAnswer((prev) => {
        const updateAnswer = [...prev];
        updateAnswer[updateAnswer.length - 1].answer = answer;
        return updateAnswer;
      });
    } catch (error) {
      console.error(error);
      setAnswer((prev) => {
        const updateAnswer = [...prev];
        updateAnswer[updateAnswer.length - 1].answer = 
        "error occuried please try again";
        return updateAnswer;
      });
    } finally {
      setLoading(false);
      setQuestion("")
    }
  };

  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop =
        chatContainerRef.current.scrollHeight;
    }
  }, [answer]);

  const clearChat = () => {
    setAnswer([]);
  };
  return (
    
    
    <div>
      
      <Navebar/>
      
      <div ref={chatContainerRef} className="conversion_box">
        {answer.length === 0 ? (
          <div className="chat_st">"Not yet message. Start your conversion"</div>
        ) : (
          answer.map((entry, index) => (
            <div key={index}>
              <br/>
              <div className="chat_you"> You : {entry.question}</div>
              <br/>
              <div className="chat_ai">AI : {entry.answer}</div>
              <br />
            </div>
          ))
        )}
        {loading && <div>AI is typing ....</div>}
      </div>

      <div className="chatbox">
        <form onSubmit={handlesubmit}>
          <input
            type="text"
            placeholder="Ask anything..."
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            required
          />
          <button type="submit" disabled={loading}>{loading ? "Submiting..." : "Submit"}</button>
          <button onClick={clearChat}>Clear Chat</button>
        </form>
      </div>
    </div>
  );
}
