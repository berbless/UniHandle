

def proccess_text(text):
    # split on space, unless between " ", or with \ before.
    # ignore \ if \\, then convert to 'litteral' (input \ as char).
    # loop until proccessed.
    special_char = False
    is_brackets = False
    output_list = []

    # .strip() to simplify the madness
    text = text.strip()

    # give the linked list an initial object
    output_list.append("")

    # for all chars of the input
    for char in text:
        # if prev char is an escape char
        if special_char:
            # append the text to the last item
            output_list[-1] += char
            # switch back to normal mode
            special_char = False
        # if current char is escape
        elif char == "\\":
            # next can be passed without problem
            special_char = True
        # if current char is 'bracket', switch bracket mode
        elif char == "\"":
            is_brackets = not is_brackets
        # if a space is inserted not in brackets
        elif char == " " and not is_brackets and not output_list[-1] == "":
            # add a new entry
            output_list.append("")
        # if none of the above, it is just a regular char, or in brackets
        elif char != " " or is_brackets:
            # append to the last item in the list
            output_list[-1] += char

    # return the now neatly organised input
    return output_list

def compile_funcs(args, wrap_hold):
    # the current func
    current_function = ""
    # the current arg
    current_arg = ""
    # that functions args
    func_args = []
    # list of functions to perform in order
    func_list = []

    try:
        # while there are still args to process
        while len(args) > 0:
            # get the next arg
            current_arg = args.pop(0)

            # pop the next to be tested.
            current_function = wrap_hold.get(current_arg)
            # Reset func args
            func_args = []

            # while the next is not a word to execute
            while len(args) > 0 and not args[0] in wrap_hold:
                # remove the next arg and add it to the list of args connected to the func
                func_args.append(args.pop(0))

            # add the packed func to the list to be executed
            current_function.set_args(func_args)
            func_list.append(current_function)

    # if a problem occurs, skip out, clear to be returned and complain at user (smh).
    except (ValueError, KeyError) as err:
        # print the err
        print(err)
        # Set out to false
        func_list = []

    # return the packed list if successfull
    return func_list