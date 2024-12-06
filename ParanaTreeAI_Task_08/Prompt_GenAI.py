import openai
from dotenv import load_dotenv
import os

load_dotenv()
open_api_key=os.getenv("OPENAI_API_KEY")
openai.api_key=open_api_key

'''1. Text Summarization '''

text = "Artificial Intelligence (AI) is one of the most transformative technologies of the 21st century, revolutionizing industries, reshaping societies, and redefining the future. At its core, AI refers to the simulation of human intelligence by machines, enabling them to perform tasks that typically require human cognition, such as problem-solving, learning, reasoning, and decision-making. This essay explores the origins of AI, its applications, benefits, challenges, and the ethical considerations surrounding its rapid advancement.The Origins and Evolution of AI.The concept of artificial intelligence dates back to ancient times when myths and legends described automatons and intelligent machines. However, AI as a scientific discipline began in the mid-20th century with pioneers like Alan Turing and John McCarthy. Turing's work on computation laid the theoretical foundation, while McCarthy coined the term artificial intelligence in 1956 during the Dartmouth Conference. Early developments focused on symbolic reasoning and rule-based systems, which eventually evolved into the machine learning and deep learning techniques that dominate AI research today.The advent of powerful computing systems, big data, and sophisticated algorithms has propelled AI into mainstream applications. Technologies like neural networks, natural language processing, and computer vision have allowed AI to surpass human capabilities in specific tasks, such as playing chess, diagnosing diseases, and even generating creative works."

prompt_sum = f"Summarize the following text: {text}"
def openai_assistant(prompt):
    response=openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role":"system","content":"your the helpful AI assistant"},
            {"role":"user","content":prompt}],
        temperature=0,
        max_tokens=200)
    return response.choices[0].message.content
summerize=openai_assistant(prompt_sum)  
# print(summerize)


''' Question & Answering '''

# context = "Generative AI models create new content like text, images, and videos based on input data."
# question = "What is generative AI?"
# prompt_OA= f"Context: {context}\nQuestion: {question}\nAnswer briefly:"
# question_answer=openai_assistant(prompt_OA)

# print(question_answer)



prompt_library = {
    "greeting": "Respond warmly to a user who greets the bot.",
    "product_info": "Provide detailed information about the product: {product_name}.",
    "troubleshooting": "Help the user resolve this issue step-by-step: {issue_description}",
    "faq_general": "Answer this FAQ question clearly: {question}.",
    "escalation": "When should I contact customer support for this problem: {problem}?"
}

# def get_response(user_query, category):
#     if category in prompt_library:
#         prompt = prompt_library[category].format(**user_query)
#         response =openai_assistant(prompt)
#         return response
#     else:
#         return "I'm not sure how to help with that."

# # Example usage
# user_query = {"product_name": "Apple IPhone"}
# category = "product_info"
# response = get_response(user_query, category)
# print(response)

