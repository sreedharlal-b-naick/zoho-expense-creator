import streamlit.web.cli as stcli
import sys


def app():
    sys.argv = [
        "streamlit",
        "run",
        "app/streamlit.py",
        "--global.developmentMode=false",
    ]
    sys.exit(stcli.main())


if __name__ == "__main__":
    app()
