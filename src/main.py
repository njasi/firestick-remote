import threading
import webview
from flaskapp.main import start_app, PORT

BASE_HEIGHT = 960
BASE_WIDTH = 240
HTML_PATH = "template/index.html"


def main():
    flask_thread = threading.Thread(target=start_app)
    flask_thread.start()

    start_webview()


def start_webview():
    print(f"Create window at {f'http://127.0.0.1:{PORT}'}")
    webview.create_window(
        title="Firestick Remote",
        url=f"http://127.0.0.1:{PORT}",
        frameless=False,
        # transparent=True,
        width=BASE_WIDTH,
        height=BASE_HEIGHT,
    )
    webview.start()


if __name__ == "__main__":
    main()
