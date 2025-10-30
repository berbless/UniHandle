from unihandle import UniHandle

def fish(test):
    """Give a sad fish a name | test function"""
    print(f"TEST FISH: {test}")

# Default main func starter.
if __name__ == "__main__":
    handle = UniHandle(keep_open=True, ignore_argv=True)
    # Method: handle[key] = function
    handle["fish"] = fish
    handle()