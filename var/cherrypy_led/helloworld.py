#! /usr/bin/python

import cherrypy

class HelloWorld(object):
    @cherrypy.expose
    def index(self):
        return("<h1>Hello World</h1>")
    index.exposed = True

    
if __name__ == "__main__":
    cherrypy.config.update({'server.socket_host' : '0.0.0.0'})
    cherrypy.config.update({'server.socket_port' : 80})
    
    cherrypy.quickstart(HelloWorld())
