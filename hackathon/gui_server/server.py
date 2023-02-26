# Necessary Imports
from fastapi import FastAPI, Body            # The main FastAPI import
from fastapi.responses import HTMLResponse   # Used for returning HTML responses
from fastapi.staticfiles import StaticFiles  # Used for serving static files
import uvicorn                               # Used for running the app

# Configuration
app = FastAPI() # Specify the "app" that will run the routing
# Mount the static directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Return a static HTML page
@app.get("/", response_class=HTMLResponse)
def get_gui_html() -> HTMLResponse:
    with open("gui.html") as html:
        return HTMLResponse(content=html.read())

# Get the specified number of buffers worth of data
@app.get("/receive/{num_buffers}")
def get_receive(num_buffers) -> str:
    print(f"Requested {num_buffers} buffers worth of data!")
    return ""

# Transmit the given message though IR in Morse code
@app.post("/transmit")
def post_transmit(message: str = Body(...)):
    print(message)

# Host the server when run
if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=6543)
