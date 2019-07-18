import webbrowser

from .App import App


def mirror(input, model, visualisations=[], port=5000):
    app = App(input, model, visualisations)

    webbrowser.open_new(f'http://localhost:{port}')  # opens in default browser

    app.run(host="0.0.0.0", port=5000)
