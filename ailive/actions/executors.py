from ailive.actions.social_actions import MockedSocialActions


def execute_social_media_func(func_name, args):
    return execute_func(MockedSocialActions(), func_name, args)


def execute_func(instance, func_name, args):
    # get the function object by name
    func = getattr(instance, func_name)
    # call the function with its arguments
    func(*args)
