# Demo: how Python decorators work under the hood, before tying it back
# to @app.route in hello.py. Plain Python, no Flask.

def my_decorator(func):
    def wrapper():
        print("before")
        func()
        print("after")
    return wrapper

@my_decorator
def hello():
    print("hello")

hello()

# func = my_decorator(hello)
# func