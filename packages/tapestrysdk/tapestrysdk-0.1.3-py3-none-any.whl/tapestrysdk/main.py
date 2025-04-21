import requests

def hello():
    print("Hello from Tapestry!")

def fetch_library_data(token, folder_details):
    folder_name = folder_details.get("name")
    organisation_id = folder_details.get("org_id")
    print("Using token:", folder_name,organisation_id)

    url = "https://tapestry.familygpt.app/admin/library"
    headers = {
        "accept": "application/json, text/plain, */*",
        "authorization": f"Bearer {token}",
        "content-type": "application/json",
    }
    data = {
        "limit": 10,
        "page": 1,
        "active": "grid",
        "group_id": [],
        "organisation_id": organisation_id,
        "parent": folder_name,
    }

    # Log the token to inspect it
    print("Using token:", token)
    
    response = requests.post(url, headers=headers, json=data)
    
    # Log the response to help with debugging
    print("Response Status Code:", response.status_code)
    print("Response Body:", response.json())
    
    if response.status_code == 200:
        print(response.json())
        return response.json()
    else:
        return {"error": f"Request failed with status code {response.status_code}", "details": response.text}

