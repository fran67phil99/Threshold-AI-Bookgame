def fetch_data_from_service(api_url, params=None):
    import requests

    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {api_url}: {e}")
        return None


def send_data_to_service(api_url, data):
    import requests

    try:
        response = requests.post(api_url, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error sending data to {api_url}: {e}")
        return None


def integrate_with_database(db_connection_string, query):
    import sqlite3

    try:
        conn = sqlite3.connect(db_connection_string)
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None
    finally:
        if conn:
            conn.close()