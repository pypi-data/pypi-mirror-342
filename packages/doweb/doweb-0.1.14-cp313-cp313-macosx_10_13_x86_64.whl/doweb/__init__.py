import os

__version__ = "0.1.14"

GFP_DOWEB_HTTPS = (
    os.environ.get("GFP_DOWEB_HTTPS", os.environ.get("GFP_KWEB_HTTPS", "false")).strip()
    == "true"
)
