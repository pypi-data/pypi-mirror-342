# Computer Use SDK

This is the Python SDK for Computer Use Tool Server, allowing you to easily control the computer desktop environment from your applications.

## Installation

```bash
# Install using pip
pip install computer-use-sdk

# Or install from source code
git clone [repository-url]
cd computer-use-tool-server
pip install -e .
```

## Usage

### Basic Usage

```python
from sdk.client import ComputerUseClient

# Initialize the client
client = ComputerUseClient(base_url="http://localhost:8000")

# Get screen size
width, height = client.get_screen_size()
print(f"Screen size: {width}x{height}")

# Move mouse to screen center
client.move_mouse(width // 2, height // 2)

# Click mouse
client.click_mouse(width // 2, height // 2)

# Type text
client.type_text("Hello, World!")

# Press Enter key
client.press_key("enter")
```

### Features List

The SDK provides the following operations:

#### Mouse Operations
- `move_mouse(x, y)`: Move mouse to specified coordinates
- `click_mouse(x, y, button="left", press=False, release=False)`: Click mouse at specified position
- `press_mouse(x, y, button="left")`: Press mouse button at specified position
- `release_mouse(x, y, button="left")`: Release mouse button at specified position
- `drag_mouse(source_x, source_y, target_x, target_y)`: Drag from source position to target position
- `scroll(x, y, scroll_direction="up", scroll_amount=1)`: Scroll mouse wheel at specified position

#### Keyboard Operations
- `press_key(key)`: Press specified key
- `type_text(text)`: Type specified text

#### Screen Operations
- `take_screenshot()`: Take a screenshot
- `get_cursor_position()`: Get current cursor position
- `get_screen_size()`: Get screen size

#### System Operations
- `wait(duration)`: Wait for specified duration (milliseconds)
- `change_password(username, new_password)`: Change user password

## Examples

See [examples.py](examples.py) for more usage examples.

## Advanced Usage

### Custom API Version

```python
client = ComputerUseClient(base_url="http://your-server.com", api_version="2020-04-01")
```

### Handling Responses

Most API calls return a dictionary containing the operation result. You can check these responses to see if the operation was successful:

```python
response = client.move_mouse(100, 100)
if response.get("success"):
    print("Mouse moved successfully")
else:
    print(f"Error: {response.get('error')}")
```

## Error Handling

The SDK automatically handles HTTP errors and raises exceptions when API calls fail. You can use try/except blocks to catch these exceptions:

```python
try:
    client.move_mouse(100, 100)
except Exception as e:
    print(f"Operation failed: {e}")
```

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests. 