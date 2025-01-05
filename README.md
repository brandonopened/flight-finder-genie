# Flight Search Assistant

This application helps you find the cheapest flights using Google Flights through an automated search process.

## Setup Instructions

1. Install Python 3.8 or higher if you haven't already
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   playwright install
   ```

3. Run the Streamlit app:
   ```bash
   streamlit run src/utils/flightSearch.py
   ```

## Features

- Automated flight search using Google Flights
- Easy-to-use interface
- Real-time search results
- Dependency installation helper

## Note

Make sure you have your OpenAI API key set in your environment variables:
```bash
export OPENAI_API_KEY='your-api-key-here'
```