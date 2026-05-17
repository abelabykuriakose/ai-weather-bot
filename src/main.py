import os
from dotenv import load_dotenv
from agent import WeatherAgent

load_dotenv()

def main():
    print("\n" + "="*50)
    print("🌤️ Welcome to the Smart AI Weather Bot! 🌤️")
    print("="*50)
    
    question = input("Ask a weather question (e.g., 'Do I need an umbrella in London today?'): ")
    print()
    
    bot = WeatherAgent()
    answer = bot.run(question)
    
    print("\n" + "🤖 " + "-"*20 + " BOT RESPONSE " + "-"*20)
    print(answer)
    print("="*50 + "\n")
    
    # NEW CODE: Save the result automatically
    output_filename = "weather_report.txt"
    with open(output_filename, "w", encoding="utf-8") as file:
        file.write(f"User Question: {question}\n")
        file.write("-" * 40 + "\n")
        file.write(f"Bot Answer:\n{answer}\n")
        
    print(f"💾 Success! Weather report saved to: {output_filename}\n")

if __name__ == "__main__":
    main()