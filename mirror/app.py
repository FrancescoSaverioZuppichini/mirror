import webbrowser

from .tree import Tracer
from .server import Builder

def mirror(input, model, visualisations=[]):
    tracer = Tracer(module=model)
    tracer(input)

    builder = Builder()

    app = builder.build(input, model, tracer, visualisations)

    # webbrowser.open_new('http://localhost:5000')  # opens in default browser

    app.run(host="0.0.0.0", port=5000)

