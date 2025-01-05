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

def generate_google_flights_link(origin, destination, departure_date, return_date=None):
    base_url = "https://www.google.com/travel/flights"
    params = {
        "hl": "en",
        "curr": "USD",
        "tfs": "1",  # Enable flight search
        "f": "a",    # Show all flights
    }
    
    # Add origin and destination
    params["q"] = f"Flights from {origin} to {destination}"
    
    # Format dates as YYYY-MM-DD for Google Flights URL
    if isinstance(departure_date, datetime):
        params["d1"] = departure_date.strftime("%Y-%m-%d")
    else:
        params["d1"] = departure_date.strftime("%Y-%m-%d") if hasattr(departure_date, 'strftime') else departure_date
        
    if return_date:
        if isinstance(return_date, datetime):
            params["d2"] = return_date.strftime("%Y-%m-%d")
        else:
            params["d2"] = return_date.strftime("%Y-%m-%d") if hasattr(return_date, 'strftime') else return_date
    
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
    
    # Date inputs
    col3, col4 = st.columns(2)
    with col3:
        departure_date = st.date_input(
            "Departure Date",
            datetime(2025, 1, 12),
            min_value=datetime.now()
        )
    with col4:
        return_date = st.date_input(
            "Return Date (Optional)",
            None,
            min_value=departure_date
        )

    trip_type = "round-trip" if return_date and return_date > departure_date else "one-way"

    if st.button("Search Flights"):
        with st.spinner("Searching for flights..."):
            try:
                formatted_departure = departure_date.strftime("%d %B %Y")
                formatted_return = return_date.strftime("%d %B %Y") if return_date else None
                
                search_task = (
                    f"Find the CHEAPEST {trip_type} flight from {origin} to {destination} "
                    f"departing on {formatted_departure}"
                )
                if formatted_return:
                    search_task += f" and returning on {formatted_return}"
                search_task += ". Only return the cheapest option with its price, airline, and flight times."

                async def search_flight():
                    agent = Agent(
                        task=search_task,
                        llm=ChatOpenAI(model="gpt-4o")  # Explicitly using gpt-4o model
                    )
                    result = await agent.run()
                    return result

                result = asyncio.run(search_flight())
                st.success("Search completed!")
                
                # Display results
                st.subheader("Search Results")
                st.write(result)
                
                # Generate and display Google Flights link
                flights_link = generate_google_flights_link(
                    origin, 
                    destination, 
                    departure_date,
                    return_date if trip_type == "round-trip" else None
                )
                st.markdown(f"[View on Google Flights]({flights_link})", unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()