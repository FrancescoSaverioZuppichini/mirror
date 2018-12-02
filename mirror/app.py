import webbrowser

from .tree import Tracer
from .server import build

def mirror(input, model):
    tracer = Tracer(module=model)
    tracer(input)

    app = build(input, model, tracer)

    webbrowser.open_new('http://localhost:5000')  # opens in default browser

    app.run(host="0.0.0.0", port=5000)

