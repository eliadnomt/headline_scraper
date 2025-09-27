from pathlib import Path

from google_auth_oauthlib.flow import InstalledAppFlow

CLIENT_SECRET = str(
    Path.home()
    / "client_secret_134764691081-1s83tr73222dm11nt4ubfpraip3hicpe.apps.googleusercontent.com.json"
)
TOKEN_FILE = str(Path.home() / ".yagmail" / "eliadnomt.json")

flow = InstalledAppFlow.from_client_secrets_file(
    CLIENT_SECRET, scopes=["https://mail.google.com/"]
)
creds = flow.run_local_server(port=0)  # launches browser or prints a URL

# Save token where yagmail expects it
Path(TOKEN_FILE).parent.mkdir(parents=True, exist_ok=True)
with open(TOKEN_FILE, "w") as f:
    f.write(creds.to_json())

print(f"Token saved to {TOKEN_FILE}")
