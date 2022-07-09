import asyncio
import tornado.web
import tornado.autoreload

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("123, world")

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

async def main():
    app = make_app()
    app.listen(8080)
    tornado.autoreload.start()
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())