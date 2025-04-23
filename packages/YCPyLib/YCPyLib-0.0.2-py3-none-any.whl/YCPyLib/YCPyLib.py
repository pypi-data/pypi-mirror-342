import time

def RunTimeIt(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"[{func.__name__}] RunTime: {end - start:.4f}")
        return result
    return wrapper

@RunTimeIt
def Hello():
    print(f"Welcome to YCPyLib")


if __name__ == "__main__":
    import YCPyLib
    Hello()

