from typing import Dict, Any, Optional
import requests
from requests.exceptions import RequestException

class TLOApiError(Exception):
    pass

class TLOApi:
    BASE_URL = "https://tlo.sh/skip"

    def __init__(self, admin_key: str):
        self.admin_key = admin_key

    def search(self, **params) -> Dict[str, Any]:
        params["admin_key"] = self.admin_key
        try:
            response = requests.get(f"{self.BASE_URL}/search", params=params)
            if response.status_code == 403:
                raise TLOApiError("Invalid API key")
            elif response.status_code != 200:
                raise TLOApiError("API error occurred")
            return response.json()
        except RequestException:
            raise TLOApiError("Connection error occurred")
        except Exception:
            raise TLOApiError("Unexpected error occurred")

    def format_person_data(self, data: Dict[str, Any]) -> str:
        try:
            people = data["people"]["person"][0]["names"]
            if not people:
                return "No people found."
            
            output = []
            for p in people:
                output.append(f"Name: {p.get('Name', 'N/A')}")
                output.append(f"Age: {p.get('Age', 'N/A')}\n")
                
                output.append("Address History:")
                for a in p.get("AddressHistory", []):
                    output.append(f"- {a.get('address')} ({a.get('dates')})")
                
                output.append("\nPhones:")
                output.extend(f"- {x}" for x in p.get("Phones", []))
                
                output.append("\nRelatives:")
                output.extend(f"- {x}" for x in p.get("Relatives", []))
                
                output.append("\nAssociates:")
                output.extend(f"- {x}" for x in p.get("Associates", []))
                
                output.append("\nEmails:")
                output.extend(f"- {x}" for x in p.get("Emails", []))
                
                output.append("\nFilings:")
                output.extend(f"- {x}" for x in p.get("Filings", []))
                
                output.append("\n" + "="*50 + "\n")
            
            return "\n".join(output)
        except Exception:
            raise TLOApiError("Failed to parse response data") 