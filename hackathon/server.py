# Necessary Imports
from fastapi import FastAPI, Body            # The main FastAPI import
from fastapi.responses import HTMLResponse   # Used for returning HTML responses
from fastapi.staticfiles import StaticFiles  # Used for serving static files
import uvicorn                               # Used for running the app

# Import buffer.py
import buffer

# Configuration
app = FastAPI() # Specify the "app" that will run the routing
# Mount the static directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Return a static HTML page
@app.get("/test", response_class=HTMLResponse)
def get_test_gui_html() -> HTMLResponse:
    with open("test-gui.html") as html:
        return HTMLResponse(content=html.read())

# Return a static HTML page
@app.get("/", response_class=HTMLResponse)
def get_gui_html() -> HTMLResponse:
    with open("gui.html") as html:
        return HTMLResponse(content=html.read())

# Get the specified number of buffers worth of message
@app.get("/rx/{num_buffers}")
def get_rx(num_buffers: int) -> dict:
    try:
        response = buffer.receive(num_buffers)
        return {'response': response}
    except:
        return {'error': 'error'}

# Transmit the given message though IR in Morse code
@app.post("/tx")
def post_tx(message: str = Body(...)):
    print(message)
    buffer.transmit(message)

# Host the server when run
if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=6543)
