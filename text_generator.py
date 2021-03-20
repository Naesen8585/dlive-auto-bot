"""
Use AI TextGen to generate a response in kind based on the given input.


"""

from aitextgen import aitextgen
import random
ai=aitextgen(model="minimaxir/reddit")
#ai=aitextgen(model="minimaxir/hacker-news")
#ai=aitextgen()
def returngeneratedtext(inputtext,minsize=20, maxsize=50):
    return random.choice(ai.generate(n=1, prompt=inputtext, max_length=len(inputtext) + maxsize, return_as_list=True,
                         min_length=(len(inputtext) + minsize))).split(inputtext)[-1]