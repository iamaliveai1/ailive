"""
This module reads a list of function calls as strings and extracts the function name and arguments.
"""


def extract_args(func_call):
    func_name, args_string = func_call.split("(")
    try:
        arguments = eval("(" + args_string)
    except SyntaxError:
        raise ValueError("Invalid function call: " + func_call)
    # ensure arguments is a tuple
    if not isinstance(arguments, tuple):
        arguments = (arguments,)
    return func_name, arguments


def main():
    # given function calls as strings
    func_calls = [
        "write_post('hello world')",
        "follow_user('davidcohen')",
        "like_post('1234')",
        "write_comment('@user1', 'Thanks for following me!')",
        "write_comment('user2', 'Thanks for the like, Dave!')",
        "follow_user('user1')"
    ]

    # loop through each function call and extract function name and arguments
    for func_call in func_calls:
        func_name, args = extract_args(func_call)
        print("Function Name:", func_name)
        print("Arguments:", args)


if __name__ == "__main__":
    main()
