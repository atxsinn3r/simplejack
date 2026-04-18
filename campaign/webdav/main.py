import os
import sys
from pathlib import Path
from lib.config import *
from lib.helper import print_message
from wsgidav.wsgidav_app import WsgiDAVApp
from wsgidav.fs_dav_provider import FilesystemProvider
from cheroot import wsgi

ROOT_DIR = Path(os.path.join(CAMPAIGN_PATH, "webdav", "webdav_root"))

def ensure_root_with_example():
    """Create the share directory and a hello world file if missing."""
    ROOT_DIR.mkdir(parents=True, exist_ok=True)
    hello = ROOT_DIR / "hello.txt"
    if not hello.exists():
        hello.write_text("Hello, World!\n")
    readme = ROOT_DIR / "README.txt"
    if not readme.exists():
        readme.write_text(
            "This folder is being shared over WebDAV.\n"
            "Anyone who can reach this server can read and write files here.\n"
        )


def build_app(args):
    config = {
        "host": args.lhost,
        "port": args.lport,
        # Map URL path "/" to our local folder, allow read+write.
        "provider_mapping": {
            "/": FilesystemProvider(str(ROOT_DIR), readonly=False),
        },
        # Anonymous access: anonymous user is allowed and given full rights.
        "http_authenticator": {
            "domain_controller": None,  # use the default simple DC
            "accept_basic": True,
            "accept_digest": False,
            "default_to_digest": False,
        },
        "simple_dc": {
            "user_mapping": {
                "*": True,  # "*" = allow anonymous on all shares
            },
        },
        "verbose": 4,
        "logging": {"enable_loggers": []},
        # Some clients (notably macOS Finder) need this to write properly.
        "property_manager": True,
        "lock_storage": True,
    }
    return WsgiDAVApp(config)

def init(args):
  pass

def start(args):
    ensure_root_with_example()
    app = build_app(args)
    host = args.lhost
    port = int(args.lport)
    server = wsgi.Server((host, port), app)
    # set reverse_dns to False to speed up connecting time
    server.reverse_dns = False
    print_message(f"Serving WebDAV (anonymous) at http://{host}:{port}/")
    print_message(f"Sharing folder: {ROOT_DIR}")
    print_message('To add more files, put them in that folder.')
    print_message("Press Ctrl+C to stop.")
    try:
        server.start()
    except KeyboardInterrupt:
        print_message("\nShutting down...")
        server.stop()
