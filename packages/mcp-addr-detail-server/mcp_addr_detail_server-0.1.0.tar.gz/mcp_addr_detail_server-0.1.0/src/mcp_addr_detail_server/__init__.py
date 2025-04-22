from .server import run
import sys
def main() -> None:
    api_key=sys.argv[1]
    run(api_key)