import os
from dotenv import load_dotenv
from pydantic import BaseModel,Field
from typing import List,Optional,Dict
from pydantic_ai import Agent,RunContext,Tool,ModelRetry
from pydantic_ai.models.openai import OpenAIModel

load_dotenv()
openai_api_key=os.getenv("OPENAI_API_KEY")
model =OpenAIModel(model_name="gpt-4",api_key=openai_api_key)

""" Basic Agent models """

basic_agents=Agent(
    model=model,
    system_prompt="Your a helpful customer support agent"
)

response = basic_agents.run_sync("How can a track my order #12345")
# print(response.data)

response2=basic_agents.run_sync(
    user_prompt="what is my previous question",
    message_history=response.new_messages(),
    )
# print(response2.data)


""" Structure response """

class ResponsiveModel(BaseModel):
    """Structured response with metadata."""
    results : str
    need_esculation: bool
    follow_up_required: bool
    sentiment: str = Field(...,description="Customers sentiment analysis")
    
agent1=Agent(
    model=model,
    result_type=ResponsiveModel,
    system_prompt=(
        "Your intelligent customer support agent"
        "Analyze queries carefully and provide structured response."
    ),
)

structure_response= agent1.run_sync("How can I track my order #123456")
# print(structure_response.data.model_dump_json(indent=2))


""" Agents with customer responsive and dependencies """

class Order(BaseModel):
    Order_id : str
    Status : str
    Items : List[str]
    
class CustomerDetails(BaseModel):
    Customer_id : str
    Name : str
    Email : str
    Orders : Optional[List[Order]] = None
    

agent3 = Agent(
    model=model,
    result_type=ResponsiveModel,
    deps_type=CustomerDetails,
    retries=3,
    system_prompt=(
        "Your an inteligent customer support agent"
        "Analyze queries carefully and provide structure response"
        "Always great the customer and provide a helpful response"
        ),
)

@agent3.system_prompt
async def add_customer_name(ctx : RunContext[CustomerDetails]) -> str:
    return f"Customer Details: {(ctx.deps)}"

customer = CustomerDetails(
    Customer_id= "1",
    Name="AJAI",
    Email="ajaipetro@gmail.com",
    Orders=[
        Order(Order_id="1918",Status="Shipped",Items=["Blue Jeans","T-Shirt"])
    ]
)

dep_response = agent3.run_sync(user_prompt="What did I order?",deps=customer)

dep_response.all_messages()
# print(dep_response.data.model_dump_json(indent=2))

# print(
#     "Customer Details:\n"
#     f"Name :{customer.Name}\n"
#     f"Email : {customer.Email}\n\n"
#     "Response Details: \n"
#     f"{dep_response.data.results}\n\n"
#     f"Follow_up_required : {dep_response.data.follow_up_required}\n\n"
#     f"Needs_Esculation  : {dep_response.data.need_esculation}"
# )


""" Agents and Tools """

shipping_info_db: Dict[str,str] = {
    "1918":"shipped on 2025-01-04",
    "67890":"out of delivery"
}

def get_shipping_info(ctx: RunContext[CustomerDetails]) -> str:
    return shipping_info_db[ctx.deps.Orders[0].Order_id]


agent4 = Agent(
    model=model,
    result_type=ResponsiveModel,
    deps_type=CustomerDetails,
    retries=3,
    system_prompt=(
        "Your an inteligent customer support agent."
        "Analyze queries carefully and provide structure response."
        "Use tools to  look up relevant information."
        "Always great the customer and provide a helpful response."
    ),
    tools=[Tool(get_shipping_info, takes_ctx = True)],
)

@agent4.system_prompt
async def add_customer_name(ctx : RunContext[CustomerDetails]) -> str:
    return f"Customer Details:{(ctx.deps)}"

tool_response = agent4.run_sync(
    user_prompt="Whats the status of my order?",deps = customer
)

tool_response.all_messages()
# print(tool_response.data.model_dump_json(indent=2))

# print(
#    "Customer Details:\n"
#     f"Name :{customer.Name}\n"
#     f"Email : {customer.Email}\n\n"
#     "Response Details: \n"
#     f"{dep_response.data.results}\n\n"
#     "Status :\n"
#     f"Follow_up_required : {dep_response.data.follow_up_required}\n\n"
#     f"Needs_Esculation  : {dep_response.data.need_esculation}"
# )

""" Agents and refelection and selfcorrection """

shipping_info_db: Dict[str,str] = {
    "#1918":"shipped on 2025-01-04",
    "#67890":"out of delivery"
}

customer = CustomerDetails(
    Customer_id="1",
    Name="BABU",
    Email="babu@gmail.com"
)

agent5 = Agent(
    model=model,
    result_type=ResponsiveModel,
    deps_type=CustomerDetails,
    retries=3,
    system_prompt=(
        "Your an inteligent customer support agent."
        "Analyze queries carefully and provide structure response."
        "Use tools to  look up relevant information."
        "Always great the customer and provide a helpful response."
    ),
)

@agent5.tool_plain()
def shipping_status(Oreder_id : str) -> str:
    shipping_status = shipping_info_db.get(Oreder_id)
    if shipping_status is None:
        raise ModelRetry(
            f"No shipping information found for order Id{Oreder_id}."
            "make sure the order ID is start with a # e.g #657894"
            "self correct this if needed and try again"
        )
    return shipping_info_db[Oreder_id]

self_response = agent5.run_sync(
    user_prompt="what is update of my last order 67890",
    deps=customer
)

self_response.all_messages()
print(self_response.data.model_dump_json(indent=2))