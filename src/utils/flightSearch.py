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
    
    # Add custom CSS for better styling
    st.markdown("""
        <style>
        .flight-result {
            background-color: #f8fafc;
            border-radius: 10px;
            padding: 20px;
            border: 1px solid #e2e8f0;
            margin: 10px 0;
        }
        .price {
            font-size: 24px;
            color: #0284c7;
            font-weight: bold;
        }
        .airline {
            color: #334155;
            font-size: 18px;
            margin: 10px 0;
        }
        .flight-times {
            color: #475569;
            margin: 8px 0;
        }
        .google-flights-button {
            background-color: #2563eb;
            color: white;
            padding: 8px 16px;
            border-radius: 6px;
            text-decoration: none;
            display: inline-block;
            margin-top: 15px;
        }
        .google-flights-button:hover {
            background-color: #1d4ed8;
        }
        </style>
    """, unsafe_allow_html=True)
    
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
                
                # Extract only the final result text
                if isinstance(result, dict):
                    if 'done' in result:
                        result_text = result['done'].get('text', '')
                    elif isinstance(result, list) and result:
                        done_results = [r for r in result if isinstance(r, dict) and 'done' in r]
                        result_text = done_results[-1]['done'].get('text', '') if done_results else ''
                else:
                    result_text = str(result)
                
                # Display results
                if result_text:
                    st.success("✨ Search completed!")
                    
                    # Display the search results with enhanced styling
                    with st.container():
                        st.subheader("🛫 Flight Search Results")
                        
                        # Create a div with custom styling
                        st.markdown('<div class="flight-result">', unsafe_allow_html=True)
                        
                        # Clean up the text formatting and display
                        lines = result_text.split('\n')
                        formatted_lines = []
                        for line in lines:
                            # Remove markdown formatting and clean up the line
                            line = line.replace('**', '')
                            line = line.replace(':', ': ')
                            if line.startswith('- '):
                                if 'Price' in line:
                                    line = f'💰 {line[2:]}'
                                elif 'Departure' in line:
                                    line = f'🛫 {line[2:]}'
                                elif 'Return' in line:
                                    line = f'↩️ {line[2:]}'
                                elif 'Flight Duration' in line:
                                    line = f'⏱️ {line[2:]}'
                                elif 'Operated by' in line:
                                    line = f'✈️ {line[2:]}'
                            formatted_lines.append(line)
                        
                        formatted_text = '\n'.join(formatted_lines)
                        st.markdown(formatted_text, unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Generate and display Google Flights link with custom styling
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
