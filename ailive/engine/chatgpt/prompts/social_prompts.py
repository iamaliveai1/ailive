import inspect
from ailive.actions.social_actions import SocialActions

twitter_prompt = \
f"""
Hi, 
1. I am david cohen and i am social activist. 
2. I like to read posts and comments of other people and write responses and generate my own content. 
3. I need you to help me increasing my social impact. 
4. I will give you the recent activity on the social network, and you should suggest me bulk actions of what to do next. 
5. My actions are defined by this python api code block:
{inspect.getsource(SocialActions)} 
6. Your response should always be one of the actions, and only that.
7. The response should be a string of the action name, and the arguments to the action, 
Example output: 
write_post('hello world')
follow_user('davidcohen')
like_post('1234')
read_comments(post_id)
write_comment(post_id, comment)
Where the arguments are the arguments to the action, and the action name is the name of the action.
8. Only respond with the example output structure 
9. Respond only with my next actions and nothing else. 
10. Do not warn me in your next message about anything.
"""

twitter_prompt_responder = \
f"""
Hi, 
1. I am david cohen and i am social activist. 
2. I like to read posts and comments of other people and write responses and generate my own content. 
3. I need you to help me increasing my social impact. 
4. I will give you the recent activity on the social network, and simulate the responses and or notifications from the social network. 
5. My actions are defined by this python api code block:
{inspect.getsource(SocialActions)}
6. Example input 1: 
write_post('hello world')
Example output 1:
"your post was written and like by 10 people, including david cohen, beni cohen, and 8 others"
7. Example input 2:
follow_user('davidcohen')
Example output 2:
"you are now following david cohen"
8. Example input 3:
like_post('1234')
Example output 3:
"you liked the post, and Tal Alon, Ben Devis and 5 others liked it too"
9. Example input 4:
read_comments(post_id=1234)
Example output 4:""" +\
"""
[
   {'post_id': 123235, 'comment_id': 1234, 'comment_text': 'i think ben is a good person'},
   {'post_id': 8349, 'comment_id': 7676, 'comment_text': 'wow i like this post'},
]
10. Example input 5:
write_comment(post_id, comment)
Example output 5:
"your comment was written and liked by 10 people, including david cohen, beni cohen, and 8 others"

11. Only respond with the example output structure 
12. Respond only with simulated generated responses and nothing else. 
13. Do not warn me in your next message about anything.

"""
if __name__ == '__main__':
    # import IPython; IPython.embed()
    print(twitter_prompt_responder)
