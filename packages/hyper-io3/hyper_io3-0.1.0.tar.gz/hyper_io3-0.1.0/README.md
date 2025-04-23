# HyperIO

**HyperIO** is a fast and flexible HTTP client for Python, supporting both synchronous and asynchronous requests. It includes built-in methods for handling login, registration, file downloads, and HTML rendering. Perfect for making fast and clean HTTP requests in any Python project.

## Features

- **Synchronous and Asynchronous HTTP Requests** (GET, POST, PUT, DELETE)
- **Login and Register Functions**
- **HTML Rendering with BeautifulSoup**
- **File Downloads** (Sync and Async)
- **Customizable Headers and Sessions**

## Installation

To install **HyperIO**, you can use pip:

```bash
pip install hyperio
```
## Usage

```python
# Importing the required classes from the hyperio package
import hyperio
from hyperio import HyperIO, AsyncHyperIO

# Synchronous Example - Using HyperIO
def sync_usage():
    print("Synchronous HTTP Request Example:")
    
    # Create a synchronous client
    client = HyperIO()

    # Making a GET request
    response = client.get("https://jsonplaceholder.typicode.com/posts/1")
    if response.ok:
        print("GET Response:", response.json())
    else:
        print("Failed to retrieve data")
    
    # Making a POST request
    data = {"title": "foo", "body": "bar", "userId": 1}
    post_response = client.post("https://jsonplaceholder.typicode.com/posts", json=data)
    if post_response.ok:
        print("POST Response:", post_response.json())
    else:
        print("Failed to post data")
    
    # HTML rendering using the view_html function
    html_content = client.view_html("https://example.com")
    print("HTML Content (first 200 chars):", html_content[:200])
    
    # File download example (sync)
    client.download_file("https://www.example.com/somefile.txt", "somefile.txt")
    print("File downloaded successfully.")

# Asynchronous Example - Using AsyncHyperIO
import asyncio

async def async_usage():
    print("\nAsynchronous HTTP Request Example:")
    
    # Create an asynchronous client
    client = AsyncHyperIO()

    # Making a GET request asynchronously
    response = await client.get("https://jsonplaceholder.typicode.com/posts/1")
    if response['ok']:
        print("GET Response:", response['json'])
    else:
        print("Failed to retrieve data")

    # Making a POST request asynchronously
    data = {"title": "foo", "body": "bar", "userId": 1}
    post_response = await client.post("https://jsonplaceholder.typicode.com/posts", json=data)
    if post_response['ok']:
        print("POST Response:", post_response['json'])
    else:
        print("Failed to post data")
    
    # HTML rendering asynchronously using the view_html function
    html_content = await client.view_html("https://example.com")
    print("HTML Content (first 200 chars):", html_content[:200])
    
    # File download example (async)
    await client.download_file("https://www.example.com/somefile.txt", "somefile_async.txt")
    print("File downloaded successfully.")
    
    # Closing the client session
    await client.close()

# Running the examples
if __name__ == "__main__":
    sync_usage()  # Run the synchronous example
    asyncio.run(async_usage())  # Run the asynchronous example
```