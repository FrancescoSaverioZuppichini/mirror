import webbrowser

from .App import App


def mirror(input, model, visualisations=[], port=5000, debug=False):
    app = App(input, model, visualisations)
    if not debug: webbrowser.open_new(f'http://localhost:{port}')  # opens in default browser
    app.run(host="0.0.0.0", port=port,  use_reloader=debug)

