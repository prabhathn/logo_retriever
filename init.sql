-- INITIAL SQL TO SET UP THE SNOWFLAKE NETWORK RULES AND EXTERNAL ACCESS INTEGRATIONS

-- CREATE API AND NETWORK INTEGRATIONS

CREATE OR REPLACE NETWORK RULE clearbit_logo
    MODE = EGRESS
    TYPE = HOST_PORT
    VALUE_LIST = ('logo.clearbit.com');

CREATE OR REPLACE NETWORK RULE clearbit_info
    MODE = EGRESS
    TYPE = HOST_PORT
    VALUE_LIST = ('autocomplete.clearbit.com');

 CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION clearbit_logo_access_integration
    ALLOWED_NETWORK_RULES = (clearbit_logo, clearbit_info)
    ENABLED = true;


-- TEST FUNCTION
CREATE OR REPLACE FUNCTION query_clearbit(query STRING)
RETURNS STRING
LANGUAGE PYTHON
RUNTIME_VERSION = 3.8
HANDLER = 'process_query'
EXTERNAL_ACCESS_INTEGRATIONS = (clearbit_logo_access_integration)
PACKAGES = ('requests')
AS 
$$
import requests
import json
session = requests.Session()
URL_PREFIX_INFO = 'https://autocomplete.clearbit.com/v1/companies/suggest?query='

def process_query(query): 
    q = query.strip()
    urls = list()
    
    results = requests.get(URL_PREFIX_INFO + q).json()
            
    return json.dumps(results)
$$;
