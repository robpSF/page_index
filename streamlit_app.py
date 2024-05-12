import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

def create_html_index(url):
    try:
        # Fetching the webpage content
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract the base URL to append to IDs
        parsed_url = urlparse(url)
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

        # Searching for headings with an ID
        headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'], id=True)

        # Building the HTML index
        html_index = '<h2>Page Index</h2>\n<ul>\n'
        for heading in headings:
            id = heading['id']
            text = heading.text.strip()
            # Create absolute URL for each link
            link = urljoin(base_url, f'#{id}')
            html_index += f'  <li><a href="{link}">{text}</a> - Description of the section</li>\n'

        html_index += '</ul>'
        return html_index
    except Exception as e:
        return f"Error fetching the page: {e}"

# Streamlit interface
st.title('HTML Heading Index Generator')
url = st.text_input('Enter the URL of the page:', '')

if st.button('Generate Index'):
    if url:
        index_html = create_html_index(url)
        # Display the HTML index in a code block
        st.code(index_html, language='html')
    else:
        st.write('Please enter a valid URL.')

