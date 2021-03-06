import tornado.ioloop
import tornado.web
import requests
import argparse

class MainHandler(tornado.web.RequestHandler):
	def get(self, slug):
		url = "http://osu.ppy.sh/api/{}?".format(slug)

		# Build URL with all get params
		for i in self.request.arguments:
			url += "{}={}&".format(i, self.get_argument(i))

		# Remove last &/? if needed
		url = url[:len(url)-1]

		# Send request to osu!api and get response
		try:
			resp = requests.get(url).text
			print("API request: api/{}".format(slug))
			self.write(resp)
		except:
			self.send_error()
			print("Error while getting osu!api response")
			raise

class GeneralHandler(tornado.web.RequestHandler):
	def get(self, what, slug):
		# Build URL
		url = "http://osu.ppy.sh/{}/{}".format(what, slug)

		# Send request to osu!api and get response
		try:
			resp = requests.get(url).text
			self.write(resp)
			print("General request: {}/{}".format(what, slug))
		except:
			self.send_error()
			print("Error while getting web response")
			raise

if __name__ == "__main__":
	# CLI stuff
	__author__ = "Nyo"
	parser = argparse.ArgumentParser(description="osu!api proxy for local ripple servers")
	parser.add_argument('-p','--port', help="osu!api proxy server port", required=False)
	args = parser.parse_args()

	# Get port from arguments
	if (args.port != None):
		serverPort = args.port
	else:
		serverPort = 5003

	# Start server
	print("osu!api proxy listening on 127.0.0.1:{}...".format(serverPort))
	app = tornado.web.Application([(r"/api/(.*)", MainHandler), (r"/(.*)/(.*)", GeneralHandler)])
	app.listen(serverPort)
	tornado.ioloop.IOLoop.current().start()
