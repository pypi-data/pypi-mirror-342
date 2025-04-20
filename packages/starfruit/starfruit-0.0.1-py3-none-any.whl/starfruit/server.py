import threading
import webbrowser
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, HttpUrl
from starlette.middleware.cors import CORSMiddleware

from starfruit.logger import get_logger
from starfruit.server_webview import router as webview_router
from starfruit.utils.const import API_HOST, API_PORT
from starfruit.utils.get_version import get_version

logger = get_logger(__name__)

STATIC_DIR = Path(__file__).parent / "static"

app = FastAPI(
    title="starfruit server",
    description="internal eternals",
    version="unknown",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(webview_router)


# Mount static assets directory (where Vite puts assets, js, css files)
assets_dir = STATIC_DIR / "assets"
if assets_dir.exists() and assets_dir.is_dir():
    app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

    logger.debug(f"Mounted static assets from {assets_dir}")
else:
    logger.warning(f"Static assets directory not found at {assets_dir}. Frontend failed to load.")


# --- ROUTES ---
@app.get("/")
async def root():
    """Serve the index.html as the default page"""
    index_file = STATIC_DIR / "index.html"
    if not index_file.exists():
        logger.error(f"index.html not found at {index_file}")
        # Return a simple message or a more informative JSON response
        return JSONResponse(
            {
                "error": "Frontend not built. Run 'make build' in 'webapp' directory.",
                "detail": f"Expected index.html at {index_file}",
            },
            status_code=500,
        )
    return FileResponse(index_file)


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "version": get_version(),
    }


class OpenUrlRequest(BaseModel):
    url: HttpUrl  # Use HttpUrl for basic validation


@app.post("/open_url")
async def open_url_in_browser(request: OpenUrlRequest):
    try:
        opened = webbrowser.open(str(request.url))  # Convert HttpUrl to string for webbrowser
        if opened:
            logger.info(f"Successfully requested to open URL: {request.url}")
            return {"message": f"Attempted to open URL: {request.url}"}
        else:
            logger.warning(
                f"webbrowser.open returned False for URL: {request.url}. It might not have opened."
            )
            return {
                "message": f"Attempted to open URL: {request.url}, but browser might not have opened."
            }
    except Exception as e:
        logger.error(f"Failed to open URL {request.url}: {e}", exc_info=True)
        return JSONResponse(status_code=500, content={"message": f"Error opening URL: {e}"})


# --- LIFECYCLE ---


@app.on_event("startup")
async def startup_event():
    logger.info("FastAPI startup event completed.")


@app.on_event("shutdown")
def shutdown():
    logger.info("shutting down FastAPI...")


def start_server(host=API_HOST, port=API_PORT):
    try:
        logger.debug(f"starting FastAPI server, docs: http://{host}:{port}/docs")
        uvicorn.run(app, host=host, port=port, log_level="info")
    except OSError as e:
        # Catch specific error for address in use
        if (
            e.errno == 48 or "address already in use" in str(e).lower()
        ):  # Check errno 48 for macOS/Linux
            logger.error(f"FATAL: Port {port} is already in use! Cannot start server.")
            # Optionally, re-raise or exit differently if needed
        else:
            logger.error(f"Network error starting FastAPI server: {e}")
    except Exception as e:
        logger.error(f"Error starting FastAPI server: {e}")


def run_server_in_thread(host=API_HOST, port=API_PORT):
    logger.debug(f"creating server thread for {host}:{port}")
    server_thread = threading.Thread(
        target=run_uvicorn,
        args=(app, host, port, False),
        daemon=True,  # make sure thread closes when main app closes
        name=f"FastAPI-{host}-{port}",
    )
    server_thread.start()
    logger.debug(f"server thread started with ID: {server_thread.ident}")
    return server_thread


def run_uvicorn(app, host: str, port: int, reload: bool):
    try:
        uvicorn.run(app, host=host, port=port, reload=reload, log_config=None)
        logger.debug(
            f"uvicorn.run({host}, {port}) completed (should not happen unless server stops)."
        )
    except Exception as e:
        logger.error(f"uvicorn.run({host}, {port}) CRASHED: {e}", exc_info=True)
    finally:
        logger.debug(f"exiting target function for {host}:{port}")


# serve index.html for all other paths (SPA routing pattern)
# NOTE: his MUST be the LAST route defined
@app.get("/{full_path:path}")
async def serve_index(full_path: str):
    index_file = STATIC_DIR / "index.html"
    if not index_file.exists():
        logger.error(f"index.html not found at {index_file} (requested path: /{full_path})")
        return JSONResponse(
            {
                "error": "Frontend assets not found. Run 'make build' in 'webapp' directory.",
                "detail": f"Expected index.html at {index_file}",
            },
            status_code=500,
        )
    # Check if the requested path looks like a file extension we shouldn't serve index.html for
    # This prevents backend API paths potentially clashing if not defined before this route
    # A more robust solution might involve checking if full_path matches known API prefixes
    if "." in Path(full_path).name and not full_path.endswith(".html"):
        logger.debug(f"path /{full_path} looks like a file, returning 404 for SPA catch-all")
        return JSONResponse({"detail": "Not Found"}, status_code=404)

    logger.debug(f"serving index.html for path: /{full_path}")
    return FileResponse(index_file)


# NOTE: DO NOT ADD ADDITIONAL ROUTES BELOW ROUTING CATCH-ALL
