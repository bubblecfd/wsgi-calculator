"""
For your homework this week, you'll be creating a wsgi application of
your own.

You'll create an online calculator that can perform several operations.

You'll need to support:

  * Addition
  * Subtractions
  * Multiplication
  * Division

Your users should be able to send appropriate requests and get back
proper responses. For example, if I open a browser to your wsgi
application at `http://localhost:8080/multiple/3/5' then the response
body in my browser should be `15`.

Consider the following URL/Response body pairs as tests:

```
  http://localhost:8080/multiply/3/5   => 15
  http://localhost:8080/add/23/42      => 65
  http://localhost:8080/subtract/23/42 => -19
  http://localhost:8080/divide/22/11   => 2
  http://localhost:8080/               => <html>Here's how to use this page...</html>
```

To submit your homework:

  * Fork this repository (Session03).
  * Edit this file to meet the homework requirements.
  * Your script should be runnable using `$ python calculator.py`
  * When the script is running, I should be able to view your
    application in my browser.
  * I should also be able to see a home page (http://localhost:8080/)
    that explains how to perform calculations.
  * Commit and push your changes to your fork.
  * Submit a link to your Session03 fork repository!


"""
import re
import traceback

def guide():
    page = """
    <html>Here's how to use this simple calculator...</html><br><br>
    To add 23+42, type <a href="/add/23/42">http://localhost:8080/add/23/42<a><br>
    To subtract 50-17, type <a href="/subtract/50/17">http://localhost:8080/subtract/50/17<a><br>
    To multiply 20*12, type <a href="/multiply/20/12">http://localhost:8080/multiply/20/12<a><br>
    To divide 100/5, type <a href="/divide/100/5">http://localhost:8080/divide/100/5<a><br>
    """

    return page


def add(*args):
    """ Returns a STRING with the sum of the arguments """

    page ='{}<br><a href="/">Back to the main page</a>'
    sum = 0
    for arg in args:
        sum += int(arg)

    return page.format(str(sum))


def subtract(*args):
    """ Returns a STRING with the subtraction result of the arguments """

    page ='{}<br><a href="/">Back to the main page</a>'
    result = int(args[0])-int(args[1])
    
    return page.format(str(result))


def multiply(*args):
    """ Returns a STRING with the multiplication of the arguments """

    page ='{}<br><a href="/">Back to the main page</a>'
    result = 1
    for arg in args:
        result *= int(arg)
    
    return page.format(str(result))


def divide(*args):
    """ Returns a STRING with the division of the arguments """

    page ='{}<br><a href="/">Back to the main page</a>'

    try:  
        result = int(args[0])/int(args[1])
        return page.format(str(result))
    except Exception:
        return page.format('Error: divided by zero')


def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """

    funcs = {
        '': guide,
        'add': add,
        'subtract': subtract,
        'multiply': multiply,
        'divide': divide
    }

    path = path.strip('/').split('/')

    func_name = path[0]
    args = path[1:]

    try:
        func = funcs[func_name]
    except KeyError:
        raise NameError

    return func, args

def application(environ, start_response):
    # TODO (bonus): Add error handling for a user attempting
    # to divide by zero.

    headers = [('Content-type', 'text/html')]

    try:
        path = environ.get('PATH_INFO', None)
        
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        body = func(*args)
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1>Internal Server Error</h1>"
        print(traceback.format_exc())
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]
    

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
