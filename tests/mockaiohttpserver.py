import sys

from aiohttp import web

routes = web.RouteTableDef()


@routes.get('/headers')
async def hello(request):
    headers = dict(request.headers)
    headers_html = '<ul>'
    for key, value in headers.items():
        headers_html += '<li>'
        headers_html += f'{key}={value}'
        headers_html += '</li>'
    headers_html += '</ul>'
    return web.Response(text=headers_html, content_type='text/html')


app = web.Application()
app.add_routes(routes)
web.run_app(app, port=int(sys.argv[1]))