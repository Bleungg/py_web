# py_web

A simple, extensible python web server made using the http.server module.  

Functionality limited currently, but will update soon

## Run the Server

From the project root (port is provided by arg):

```sh
python3 src/py_web.py {PORT}
```

By default, the server serves files from the public directory

## Browse the Site

Default viewing of any path is the index.html

Visit any subdirectory (e.g., `/test/`) to see a directory listing if no `index.html` is present.

## POST Requests

Can use the provided utility to send a basic POST request:

With Python utility:
```sh
python src/util.py
```

Currently only JSON post requests are able to be handled
