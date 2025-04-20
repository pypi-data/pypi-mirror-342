from .timing import timer
from rich import print

if __name__ == "__main__":
    import time

    @timer
    def example_function():
        time.sleep(2)

    example_function()
