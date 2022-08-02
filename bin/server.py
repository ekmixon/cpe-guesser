#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import falcon
from wsgiref.simple_server import make_server
import json

# Configuration
port = 8000

runPath = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(runPath, ".."))
from lib.cpeguesser import CPEGuesser


class Search:
    def on_post(self, req, resp):
        data_post = req.bounded_stream.read()
        js = data_post.decode('utf-8')
        try:
            q = json.loads(js)
        except ValueError:
            resp.status = falcon.HTTP_400
            resp.media = "Missing query array or incorrect JSON format"
            return

        if 'query' not in q:
            resp.status = falcon.HTTP_400
            resp.media = "Missing query array or incorrect JSON format"
            return

        cpeGuesser = CPEGuesser()
        resp.media = cpeGuesser.guessCpe(q['query'])


if __name__ == '__main__':
    app = falcon.App()
    app.add_route('/search', Search())

    try:
        with make_server('', port, app) as httpd:
            print(f"Serving on port {port}...")
            httpd.serve_forever()
    except OSError as e:
        print(e)
        sys.exit(1)
    except KeyboardInterrupt:
        sys.exit(0)
