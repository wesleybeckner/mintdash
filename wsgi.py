"""Application entry point."""
from mintdash import init_app

debug = False

app = init_app(debug, page='visualize')

if (__name__ == "__main__") & (debug == False):
    app.run()

elif (__name__ == '__main__') & (debug == True):
    app.run_server(debug=True, port="5000")