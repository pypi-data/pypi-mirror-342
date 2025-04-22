"""
Examples for Computer Use SDK
"""
from .client import ComputerUseClient


def example_basic_operations():
    """
    Example of basic mouse and keyboard operations
    """
    # Initialize the client
    client = ComputerUseClient(base_url="http://10.37.26.209:8102")

    # MoveMouse
    # ret = client.move_mouse(100,100)
    # print(f"MoveMouse response: {ret}")
    # ret = client.click_mouse(100,120,"right")
    # print(f"ClickMouse response: {ret}")
    # client.type_text("Hello World")
    # client.press_key("enter")
    client.click_mouse(100,100,"right")

if __name__ == "__main__":
    print("Running basic operations example:")
    example_basic_operations()
