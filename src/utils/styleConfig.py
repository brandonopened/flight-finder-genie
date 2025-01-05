def get_streamlit_styles():
    """Return the custom CSS styles for Streamlit."""
    return """
        <style>
        .flight-result {
            background-color: #f8fafc;
            border-radius: 10px;
            padding: 20px;
            border: 1px solid #e2e8f0;
            margin: 10px 0;
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
    """