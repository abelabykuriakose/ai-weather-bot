from langchain_google_genai import ChatGoogleGenerativeAI
from tools import get_current_weather

class WeatherAgent:
    def __init__(self):
        # We use gemini-flash-latest because it natively supports advanced Function Calling/Tool Use
        self.llm = ChatGoogleGenerativeAI(model="gemini-flash-latest", temperature=0.2)
        
        # Bind our weather tool directly to the model
        self.tools = [get_current_weather]
        self.llm_with_tools = self.llm.bind_tools(self.tools)

    def run(self, user_question: str):
        print("🧠 Agent is analyzing your question...")
        
        # Step 1: Let the AI decide if it needs a tool
        ai_msg = self.llm_with_tools.invoke(user_question)
        
        # Step 2: Check if the AI decided to call a tool
        if ai_msg.tool_calls:
            tool_call = ai_msg.tool_calls[0]
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            
            # Execute our real Python tool function using the arguments provided by Gemini
            if tool_name == "get_current_weather":
                tool_output = get_current_weather.invoke(tool_args)
                
                # Step 3: Feed the tool results back into Gemini so it can write a friendly response
                print("📝 Agent is compiling the live data into an answer...")
                final_response = self.llm.invoke(
                    f"The user asked: '{user_question}'. You ran the weather tool and got this data: '{tool_output}'. "
                    f"Answer their question accurately based on this data. Be specific about whether they need an umbrella."
                )
                
                # Safe Extraction logic for modern LangChain payloads
                content = final_response.content
                if isinstance(content, list) and len(content) > 0:
                    if isinstance(content[0], dict) and "text" in content[0]:
                        return content[0]["text"]
                return str(content)
        else:
            # If the user asked something normal like "Hello!", no tool is needed
            return ai_msg.content