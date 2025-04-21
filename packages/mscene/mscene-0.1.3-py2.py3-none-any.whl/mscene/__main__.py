from pathlib import Path
import requests
import sys


def fetch(url):
    try:
        response = requests.get(url)
        if not response.ok:
            response = None
    except Exception:
        response = None

    return response


def main(args=None):

    if args is None:
        args = sys.argv[1:]
    elif isinstance(args, str):
        args = args.split()
    else:
        args = None

    if not args:
        args = ["-h"]

    source = "https://mscene.curiouswalk.com/mscene"
    response = fetch(f"{source}/RELEASE")

    if response:
        path = Path(__file__).parent
        release = path / "RELEASE"
        content = response.content
        if not release.exists() or release.read_bytes() != content:
            text = response.text.split()
            error = None
            for name in text[1:]:
                response = fetch(f"{source}/{name}.py")
                if response:
                    filename = path / f"{name}.py"
                    filename.write_bytes(response.content)
                else:
                    error = True
                    break

            if error is None:
                release.write_bytes(content)

    try:
        from mscene.core import execute
    except Exception:
        print("Error: Something went wrong")
    else:
        execute(args)


if __name__ == "__main__":

    main()
