import streamlit as st
from snowflake.snowpark.context import get_active_session
import snowflake.connector
import re
import json

#
# SESSION & PARAMETERS
#
session = get_active_session()
MAX_RESULTS = 1
DOMAIN_MATCH_PATTERN = "^(([a-zA-Z]{1})|([a-zA-Z]{1}[a-zA-Z]{1})|([a-zA-Z]{1}[0-9]{1})|([0-9]{1}[a-zA-Z]{1})|([a-zA-Z0-9][a-zA-Z0-9-_]{1,61}[a-zA-Z0-9]))\.([a-zA-Z]{2,6}|[a-zA-Z0-9-]{2,30}\.[a-zA-Z]{2,3})$"
URL_PREFIX_LOGO = 'https://logo.clearbit.com/'
REMOVED_TEXT = [', inc.', ', inc', '\'s']
WIDTH_SELECT = {'Auto':None, '50':50, '100':100, '200':200}
GREYSCALE_PARAM = '?greyscale=1'

#
# FUNCTION DEFINITIONS
#
def split_input(txt):
    '''Splits the input into a list of domains. With minor error checking.'''

    raw_str = txt.lower()
    for r in REMOVED_TEXT:
        raw_str = raw_str.replace(r, '')

    domains = re.split(r'[,;\n]', raw_str)
    
    return domains

def create_img_list(domains):
    '''Converts list of domains into Image URLs that pull from the clearbit API. If a domain is not provided,
    then try and resolve with Clearbit Autocomplete API.'''
        
    urls = []
    for dd in domains:
        if valid_domain(dd):
            urls.append((URL_PREFIX_LOGO + dd, dd))
        else:
            results = session.sql("select query_clearbit('{}')".format(dd)).collect()

            possible_domains = json.loads(results[0][0])
            
            # for each domain, append to urls list (grab only top N)
            for p in possible_domains[slice(MAX_RESULTS)]:
                urls.append((p['logo'], dd + ' (guess: ' + p['domain'] + ')'))
            
    return urls

def valid_domain(domain):
    '''Check string to determine if it's a valid domain'''
    
    return bool(re.match(DOMAIN_MATCH_PATTERN, domain))

#
# STREAMLIT UI CODE
#
st.title("Logo Retriever 🦮")
st.subheader("Get logos in bulk for presentations!")
st.markdown('[Logos provided by Clearbit](https://clearbit.com)')
txt = st.text_area('Enter a list of domains or search terms, separated by commas, semicolons, or new lines:', 
                   'snowflake.com,robling.io,procter gamble\nkraftheinz.com;albertsons.com\niBotta\nUnder Armour', 
                   placeholder='''Type a list of Company URLs separated by commas, semicolons, or new lines. Do not put www. in front.''')

col1, col2, col3 = st.columns(3)
with col1:
    width = st.selectbox('Default image widths (in pixels)', list(WIDTH_SELECT.keys()), index=2)

with col3:
    greyscale = st.checkbox('Greyscale images', value=False)

st.divider()

# Get list of inputs and translate to Logo URLs or autocompletes
with st.spinner('Fetching Logos...'):
    companies = split_input(txt)
    request_list = create_img_list(companies)

    # Parse (url, caption) tuples
    urls = []
    captions = []
    for r in request_list:
        if greyscale:
            url = r[0]+GREYSCALE_PARAM
        else:
            url = r[0]
        urls.append(url)
        captions.append(r[1])

# Plot matrix of logos
st.markdown("""#### Logos  
Right click and copy or save image""")
st.image(image=urls, caption=captions, width=WIDTH_SELECT[width])

# Credits and Notes
st.divider()
st.markdown("""*Known issues: Minimal error-checking on text entry, no graceful fail for 404*

Release Notes:
>1.4 - Minimal error checking for stray commas, image width and greyscale options  
>1.3 - Moved to Streamlit in Snowflake  
>1.2 - Big fixes  
>1.1 - More flexible entry to allow for domains and text  
>1.0 - Original Release  

Created by [Prabhath Nanisetty](https://www.linkedin.com/in/prabhathnanisetty). Code at [Github](https://github.com/prabhathn/logo_grabber)  
""")
