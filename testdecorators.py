def print_result(func):
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        print(str(res))
        return res
    return wrapper