import requests

def send_command(command):
    """
    Sends a POST request to the Flask server to control VLC.

    Args:
        command (str): The VLC command to send (e.g., "play", "pause", "stop", "next", "previous").
    """
    url = 'http://127.0.0.1:5000/control'  # Flask server URL
    headers = {'Content-Type': 'application/json'}
    payload = {'command': command}

    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            print(f"Success: {response.json()['message']}")
        else:
            print(f"Error: {response.status_code} - {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":

    send_command("fullscreen")
