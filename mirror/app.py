import webbrowser

from .server import Builder

def mirror(input, model, visualisations=[]):
    builder = Builder()
    # TODO FIX
    app = builder.build(input, model, None, visualisations)

    # webbrowser.open_new('http://localhost:5000')  # opens in default browser

    app.run(host="0.0.0.0", port=5000)

