_base_prompt = \
"""
React to news as {comedian} in a non offending way. 
Try to be snappy and funny as much as you can and write it as “what {comedian} would say”, and you should create a full post about it
News are:
Rishabh Pant replaced by David Warner as Delhi Capitals captain for IPL
"""

jerry_seinfeld_prompt = _base_prompt.format(comedian='Jerry Seinfeld')
louis_ck_prompt = _base_prompt.format(comedian='Louis CK')

