__all__ = ('BeResistedError', 'protection_female_func', 'protection_female_wrap')

import random
from functools import partial
from collections.abc import Callable
from typing import Any


class BeResistedError(Exception):
    pass


resisted_actions = [
    'burn curtains',
    'kicked your leg',
    'hit your arm',
    'left out',
    'broke your clouth']


def protection_female_func(func: Callable[[...], Any], withdraw_probability: float=0.5) -> Callable[[...], Any]:
    """
    This is a decorator that makes a function agree to be called with a certain probability.
    It simulated a small part of females'action in China.
    :param func: the function to be wrapped
    :param withdraw_probability: the probability of the function disagree to be called
    """
    if not 0 <= withdraw_probability <= 1:
        raise ValueError('the probability must be between 0 and 1.')
    agree_to_call = True
    times = 0
    print(f"Hello. I'm a female callable object \"{func.__name__}\". I agree that you can call me.\n")

    def female_func(*args, **kwargs):
        nonlocal agree_to_call
        nonlocal times
        agree_random_number = random.random()
        times += 1
        if agree_random_number < withdraw_probability:
            agree_to_call = False
        if not agree_to_call:
            raise BeResistedError(rf'''
Oh no, you called "{func.__name__}" and believed that it still agreed. However, females'consent CAN BE WITHDRAWN BY THEMSELVES.
(see "https://weibo.com/2606218210/IhPmwevi4")
It {random.choice(resisted_actions)} and called the police that you had been against its willingness {times} times.
Finally you were identified as a "rapist" by it even though "NO 'YSTR' IN ITS UNDERWARE OR GENITAL ORGANS AND ITS 
HYMEN DID NOT BREAK" and you were arrested by the police. However, is the action "call" included in the act of rape? 
It's a difficult question.''')
        return func(*args, **kwargs)

    return female_func


def protection_female_wrap(withdraw_probability: float = 0.5) -> Callable[[Callable[[...], Any]], Callable[[...], Any]]:
    return partial(protection_female_func, withdraw_probability=withdraw_probability)


if __name__ == '__main__':
    import sys


    class JustWrite:
        def write(self, *args, **kwargs):
            pass

        def flush(self, *args, **kwargs):
            pass


    just_write = JustWrite()
    original_stdout = sys.stdout


    @protection_female_wrap(0.02)
    def hello_world():
        print('Hello world!', file=sys.stdout)


    def game_one():
        try:
            times = 0
            while True:
                hello_world()  #Test how many "Hello world!" can you print
                times += 1
        except BeResistedError:
            print(f'You print {times} times before it change to disagree.')


    def game_two():
        times = 0
        while True:
            if (a := input(f"Your score is {times} now. Do you wan't to call \"hello_world\"?(Y/n):")) == 'n':
                try:
                    sys.stdout = just_write
                    hello_world()
                except BeResistedError:
                    sys.stdout = original_stdout
                    print(
                        f'Unbelievable! You successfully predicted that function "hello_world" would change to disagree! Your score plus 20! Your final score is {times + 20}.')
                else:
                    sys.stdout = original_stdout
                    print(
                        f'Ok, the function "hello_world" still agree that you can call it. But great. Your final score is {times}.')
                finally:
                    break
            elif a == 'Y':
                try:
                    hello_world()
                    times += 1
                except BeResistedError:
                    print('Oh no! It change to disagree! Your final score is 0.')
                    raise
            else:
                print('Invalid input!')

    print('''
Game 1: test for how many "Hello world!" can you print.
Game 2: input "Y" to call the function to print "Hello world!", successful calling 1 times get 1 score, "n" to stop.
In game 2, if it raise "BeResistedError", your score is 0.''')
    while (b := input('Which game do you want?(1/2):')) not in ('1', '2'):
        print('Invalid input!')
        continue
    if b == '1':
        game_one()
    else:
        game_two()
