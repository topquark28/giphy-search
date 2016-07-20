#!/usr/bin/env python

import json
import jinja2
import logging
import urllib
import webapp2
from google.appengine.api import urlfetch


class MainHandler(webapp2.RequestHandler):

    def get(self):
        self.response.write("Please use the search page.")


class SearchHandler(webapp2.RequestHandler):

    def get(self):
        """Respond to HTML GET requests"""
        logging.info("===== %s.get()" % self.__class__.__name__)
        #
        template = jinja_env.get_template('search.html')
        self.response.write(template.render())


class ResultsHandler(webapp2.RequestHandler):

    def get(self):
        """Respond to HTML GET requests"""
        logging.info("===== %s.get()" % self.__class__.__name__)
        #
        template = jinja_env.get_template('results.html')
        #
        term = self.request.get('term')
        if term:
            gifs = self.fetch_gifs(term)
            variables = {
                'name': self.request.get('name'),
                'search_term': term,
                'image_urls': gifs
            }
            self.response.write(template.render(variables))
        else:
            self.response.write("Please specify a search term.")

    def fetch_gifs(self, term):
        """Use the Giphy API to fetch image URLs."""
        logging.info("===== %s.get()" % self.__class__.__name__)
        #
        data_source = urlfetch.fetch(self.giphy_search(term))
        results = json.loads(data_source.content)
        #
        gifs = []
        for gif_entry in results['data']:
            gifs.append(gif_entry['images']['original']['url'])
        #
        return gifs

    def giphy_search(self, term):
        """Construct a URL for searching in the Giphy API."""
        logging.info("===== %s.get()" % self.__class__.__name__)
        #
        GIPHY_API_KEY = 'dc6zaTOxFJmzC'
        base_url = 'http://api.giphy.com/v1/gifs/search?'
        url_params = {
            'q': term,
            'api_key': 'dc6zaTOxFJmzC',
            'limit': 10,
        }
        full_url = base_url + urllib.urlencode(url_params)
        #
        logging.info("===== full_url is %s" % (full_url))
        return full_url


jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))
routes = [
    ('/', MainHandler),
    ('/search', SearchHandler),
    ('/results', ResultsHandler),
]
app = webapp2.WSGIApplication(routes, debug=True)
