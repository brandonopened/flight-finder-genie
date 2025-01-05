from langchain_openai import ChatOpenAI
from browser_use import Agent
import asyncio
import streamlit as st
import subprocess
import sys
from datetime import datetime
from urllib.parse import urlencode
from formatFlightResult import format_flight_result
from styleConfig import get_streamlit_styles

def install_dependencies():
    """Install required packages and playwright."""
    subprocess.check_call([sys.executable, "-m", "pip", "install", "browser-use", "langchain-openai"])
    subprocess.check_call([sys.executable, "-m", "playwright", "install"])

def generate_google_flights_link(origin, destination, departure_date, return_date=None):
    """Generate a Google Flights URL with search parameters."""
    base_url = "https://www.google.com/travel/flights"
    params = {
        "hl": "en",
        "curr": "USD",
        "tfs": "1",
        "f": "a",
    }
    
    params["q"] = f"Flights from {origin} to {destination}"
    
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
    """Main function to run the Streamlit app."""
    st.set_page_config(page_title="Flight Search Assistant", page_icon="✈️")
    st.markdown(get_streamlit_styles(), unsafe_allow_html=True)
    
    st.title("Flight Search Assistant")
    
    if st.button("Install Dependencies"):
        with st.spinner("Installing required packages..."):
            try:
                install_dependencies()
                st.success("Dependencies installed successfully!")
            except Exception as e:
                st.error(f"Failed to install dependencies: {str(e)}")
                return

    # Input fields
    col1, col2 = st.columns(2)
    with col1:
        origin = st.text_input("From", "Eugene, OR")
    with col2:
        destination = st.text_input("To", "Seattle, WA")
    
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
            datetime(2025, 1, 17),
            min_value=departure_date
        )

    trip_type = "round-trip" if return_date and return_date > departure_date else "one-way"

    if st.button("Search Flights"):
        search_placeholder = st.empty()
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
                        llm=ChatOpenAI(model="gpt-4o")
                    )
                    result = await agent.run()
                    return result

                result = asyncio.run(search_flight())
                
                # Format and display results
                if result:
                    st.success("✨ Search completed!")
                    
                    with st.container():
                        st.subheader("🛫 Flight Search Results")
                        st.markdown('<div class="flight-result">', unsafe_allow_html=True)
                        
                        formatted_text = format_flight_result(result)
                        st.markdown(formatted_text)
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Generate and display Google Flights link
                    flights_link = generate_google_flights_link(
                        origin, 
                        destination, 
                        departure_date,
                        return_date if trip_type == "round-trip" else None
                    )
                    st.markdown(f'<a href="{flights_link}" target="_blank" class="google-flights-button">🔍 View on Google Flights</a>', unsafe_allow_html=True)
                else:
                    st.error("No flight results found. Please try again.")
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()