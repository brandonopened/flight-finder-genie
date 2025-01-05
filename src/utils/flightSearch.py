from langchain_openai import ChatOpenAI
from browser_use import Agent
import asyncio
import streamlit as st
import subprocess
import sys
from datetime import datetime
from urllib.parse import urlencode

def install_dependencies():
    subprocess.check_call([sys.executable, "-m", "pip", "install", "browser-use", "langchain-openai"])
    subprocess.check_call([sys.executable, "-m", "playwright", "install"])

def generate_google_flights_link(origin, destination, date):
    base_url = "https://www.google.com/travel/flights"
    params = {
        "q": f"Flights from {origin} to {destination} on {date}",
        "hl": "en"
    }
    return f"{base_url}?{urlencode(params)}"

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

    # Add input fields
    col1, col2 = st.columns(2)
    with col1:
        origin = st.text_input("From", "Bali")
    with col2:
        destination = st.text_input("To", "Oman")
    
    date = st.date_input(
        "Travel Date",
        datetime(2025, 1, 12),
        min_value=datetime.now()
    )

    if st.button("Search Flights"):
        with st.spinner("Searching for flights..."):
            try:
                formatted_date = date.strftime("%d %B %Y")
                async def search_flight():
                    agent = Agent(
                        task=f"Find a one-way flight from {origin} to {destination} on {formatted_date} on Google Flights. Return me the cheapest option with the price, departure time, arrival time, and airline.",
                        llm=ChatOpenAI(model="gpt-4"),
                    )
                    result = await agent.run()
                    return result

                result = asyncio.run(search_flight())
                st.success("Search completed!")
                
                # Display results
                st.subheader("Search Results")
                st.write(result)
                
                # Generate and display Google Flights link
                flights_link = generate_google_flights_link(origin, destination, formatted_date)
                st.markdown(f"[View on Google Flights]({flights_link})", unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()