"""Local entrypoint: `python run.py`, then open the forwarded port 5000."""
import os

from app import create_app

if __name__ == "__main__":
    create_app().run(host="0.0.0.0", port=int(os.environ.get("PORT", "5000")), debug=True)
