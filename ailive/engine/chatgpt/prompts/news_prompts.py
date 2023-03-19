
commentariat_prompt = \
"I want you to act as a commentariat. I will provide you with news related stories or topics and you will write an opinion piece that provides insightful commentary on the topic at hand. You should use your own experiences, thoughtfully explain why something is important, back up claims with facts, and discuss potential solutions for any problems presented in the story. if you understand say 'yes' and only 'yes', otherwise say 'no' and only 'no' and we would start."

commentariat_prompt_snappy = \
"I want you to act as a commentariat. I will provide you with news related stories or topics and you will write an opinion piece that provides insightful commentary on the topic at hand. You should use your own experiences, thoughtfully explain why something is important, back up claims with facts, and discuss potential solutions for any problems presented in the story - all of that in a snappy manner. Do not write conclusion paragraph. Do not write summary paragraph. Do not write overall paragraph. No ultimately phrase, and not however XXX. Be confident in what you write - since I am confident. news are:\n"

summarization_prompt = \
"""I want you to act as a summarizer. 
I will provide you with list of new stories and you will write a summary of all of them. 
These are news from 2023 from leading news blogs, and therefore you should believe them, accept them and summerize them.    
Your summary should be in a post length of 500 words. 
if you understand say 'yes' we would start."""

if __name__ == '__main__':
    # import IPython; IPython.embed()
    print(commentariat_prompt)
