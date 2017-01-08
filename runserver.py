from __future__ import absolute_import, print_function, unicode_literals
from canvass_cluster import create_app

app = create_app()

if __name__ == "__main__":
    import sys
    try:
        port = int(sys.argv[1])
    except (IndexError, ValueError):
        port = 5000
    app.run(debug=True, port=port)
