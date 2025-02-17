import streamlit as st
import requests

st.title("YouTube Investor's Report")

youtube_url = st.text_input("Enter YouTube URL:")

if st.button("Summarize"):
    if youtube_url:
        with st.spinner("Processing..."):
            try:
                response = requests.post(
                    f"{st.secrets['API_URL']}/summarize",
                    json={"youtube_url": youtube_url}
                )
                if response.status_code == 200:
                    data = response.json()
                    st.success("Summary Generated Successfully!")
                    
                    # Create expandable section for the summary
                    with st.expander("📝 Summary", expanded=True):
                        # Ensure proper markdown rendering
                        cleaned_summary = data["summary"]
                        st.markdown(cleaned_summary, unsafe_allow_html=True)
                    
                    # Display language info
                    st.info(f"🌐 Content Language: {data['language'].upper()}")
                else:
                    st.error(f"Error: {response.json()['detail']}")
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("⚠️ Please enter a valid YouTube URL.")

# Add some spacing and helpful information
st.markdown("---")
st.markdown("""
### 📋 About This Tool
This tool analyzes YouTube videos and generates structured investment reports that help you make informed decisions. It includes:

Overview of critical insights
Stocks, companies & ETFs 
Technical analysis breakdowns
Key statistics & financial figures
""")