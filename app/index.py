from mod_python import apache

def handler(req):
    req.send_http_header()
    req.write("Hello world");
    return apache.OK
