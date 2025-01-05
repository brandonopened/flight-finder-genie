from langchain_openai import ChatOpenAI
from browser_use import Agent
import asyncio
import streamlit as st
import subprocess
import sys

def install_dependencies():
    subprocess.check_call([sys.executable, "-m", "pip", "install", "browser-use", "langchain-openai"])
    subprocess.check_call([sys.executable, "-m", "playwright", "install"])

def main():
    st.set_page_config(page_title="Flight Search Assistant", page_icon="✈️")
    
    st.title("Flight Search Assistant")
    
    if st.button("Install Dependencies"):
        with st.spinner("Installing required packages..."):
            try:
                install_dependencies()
                st.success("Dependencies installed successfully!")
            except Exception as e:
                st.error(f"Failed to install dependencies: {str(e)}")
                return

    if st.button("Search Flights"):
        with st.spinner("Searching for flights..."):
            try:
                async def search_flight():
                    agent = Agent(
                        task="Find a one-way flight from Bali to Oman on 12 January 2025 on Google Flights. Return me the cheapest option.",
                        llm=ChatOpenAI(model="gpt-4o"),
                    )
                    result = await agent.run()
                    return result

                result = asyncio.run(search_flight())
                st.success("Search completed!")
                st.write(result)
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()