from unihandle import UniHandle, In_Opt, Out_Opt

def fish(test):
    """Give a sad fish a name | test function"""
    print(f"TEST FISH: {test}")

# Default main func starter.
if __name__ == "__main__":
    handle = UniHandle(in_opt=In_Opt.BOTH, out_opt=Out_Opt.MENU)
    # Method: handle[key] = function
    handle["fish"] = fish
    handle()