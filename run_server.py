"""Server runner for CodeForge autonomous web application."""

import sys
import uvicorn

if __name__ == "__main__":
    port = 8000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            pass
    print(f"Starting CodeForge Autonomous Web Application on http://localhost:{port}...")
    uvicorn.run("app.main:app", host="127.0.0.1", port=port, log_level="info", reload=False)
