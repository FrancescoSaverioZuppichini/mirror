import webbrowser

from .server import Builder

def mirror(input, model, visualisations=[]):
    builder = Builder()

    app = builder.build(input, model, visualisations)

    webbrowser.open_new('http://localhost:5000')  # opens in default browser

    app.run(host="0.0.0.0", port=5000, use_reloader=True)

