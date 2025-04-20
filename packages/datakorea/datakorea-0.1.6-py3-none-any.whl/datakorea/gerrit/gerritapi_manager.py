import requests
import json

class GerritAPIManager:
    def __init__(self, base_url, username, password):
        self.base_url = base_url.rstrip('/')
        self.auth = (username, password)

    def get_all_changes(self):
        endpoint = "changes/?q=is:open+owner:self&q=is:open+reviewer:self+-owner:self&o=LABELS"
        url = f"{self.base_url}/a/{endpoint}"
        print(url)
        response = requests.get(url, auth=self.auth)
        if response.status_code == 200:
            # Parse the JSON response
            try:
                cleaned_text = response.text.lstrip(")]}'\n")

                change_details = json.loads(cleaned_text)

                commit_list = []
                for change in change_details[1]:
                    # print(f"change : {change}")

                    commit_item = {
                    }
                    for key, value in change.items():

                        if key == "id":
                            commit_item["change_id"] = value
                        elif key == "project":
                            commit_item["project"] = value
                        elif key == "branch":
                            commit_item["branch"] = value

                        commit_list.append(commit_item)

                    # print(commit_list)
                return commit_list
            except json.JSONDecodeError:
                print("Failed to decode JSON response")
                return None
        else:
            print(f"Failed to fetch change details: {response.status_code}")
            return None
