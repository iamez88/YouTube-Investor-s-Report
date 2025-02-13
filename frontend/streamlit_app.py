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
                    st.success("Summary:")
                    st.write(data["summary"])
                    st.info(f"Language: {data['language']}")
                else:
                    st.error(f"Error: {response.json()['detail']}")
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a valid YouTube URL.")
