import requests

class APIClient:
    def __init__(self, api_key):
        # Initialize the API client with your API key
        self.api_key = api_key
        self.base_url = "https://api.example.com"  # Replace with the actual base URL of the API
    
    def _get_headers(self):
        # Include the API key in the request headers (modify if needed)
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def get_data(self, endpoint):
        # Make a GET request to the specified endpoint
        url = f"{self.base_url}/{endpoint}"
        try:
            response = requests.get(url, headers=self._get_headers())
            response.raise_for_status()  # Raise an error for bad responses (e.g., 404, 500)
            return response.json()  # Return the JSON response
        except requests.exceptions.RequestException as e:
            print(f"Error occurred: {e}")
            return None

    def post_data(self, endpoint, data):
        # Make a POST request to the specified endpoint with the provided data
        url = f"{self.base_url}/{endpoint}"
        try:
            response = requests.post(url, json=data, headers=self._get_headers())
            response.raise_for_status()  # Raise an error for bad responses
            return response.json()  # Return the JSON response
        except requests.exceptions.RequestException as e:
            print(f"Error occurred: {e}")
            return None

# Example usage:
if __name__ == "__main__":
    # Replace with your actual API key
    api_key = "your_api_key_here"  
    client = APIClient(api_key)

    # Make a GET request (example endpoint)
    data = client.get_data("some-endpoint")  # Replace "some-endpoint" with actual endpoint
    if data:
        print("Data received:", data)

    # Make a POST request (example endpoint)
    post_data = {"key": "value"}  # Replace with the actual data to send
    response = client.post_data("another-endpoint", post_data)  # Replace with actual endpoint
    if response:
        print("Post response:", response)
