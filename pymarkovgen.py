# PyMarkovGen
# For Python 3.5
# By Aurélien Antoine
# v 0.0.1 2016

# A simple Markov Chains generator working with numbers.
# Based on PyMarkov 0.1.0 by Slater Victoroff (http://pypi.python.org/pypi/PyMarkov/).


from collections import Counter
import random
import itertools


def splitsource(entry):
    # Basic callback, splits the list on spaces
    return [number for number in entry.split()]


def norder_markov(entry, norder, current_dict, split_callback):
    # Updates the current markov dictionary based on the given entry
    source = split_callback(entry)
    for i in range(0, len(source) - norder):
        current_tuple = tuple([source[j] for j in range(i, i + norder)])
        if current_dict.get(current_tuple, False):
            current_dict[current_tuple].update([source[i + norder]])
        else:
            current_dict[current_tuple] = Counter([source[i + norder]])
    return current_dict


def train(source, norder, split_callback=splitsource):
    # Creates the master markov chain reference dictionary

    # norder sets the length of look-behind for markov chain generation.
    # 1-order means only based on the current number, 2-ord means based on the current and previous number, etc...

    # The split_callback is an optional argument that allows you to define how the program turns a line of text
    # into a list of words. The default just casts to ascii and splits on spaces.

    master_dict = {i: {} for i in range(1, norder + 1)}
    for line in source:
        for key, value in master_dict.items():
            master_dict[key] = norder_markov(line, key, value, split_callback)
    return master_dict


def get_check_tuple(current_output, norder):
    # Gets a tuple of all tokens to consider in generating the next element

    last_n_list = [current_output[-i] for i in range(1, norder + 1)]
    last_n_list.reverse()
    return tuple(last_n_list)


def append_next_value(master_dict, current_output, norder):
    # Adds the next value to the output

    norder = min(len(current_output), norder)
    norder_list = []
    for i in range(1, norder + 1):
        check = master_dict[i].get(get_check_tuple(current_output, i), {})
        norder_list.extend([[key] * value * i for key, value in check.items()])
    master_list = list(itertools.chain(*norder_list))
    current_output.append(random.choice(master_list))


def generate(source, output_length, norder, join_char=" "):
    # Given a master dictionary, returns a generated Markov Chain of tokens

    source2 = list(map(int, source.replace(' ', '')))
    master_dict = train([source], norder)
    output = []
    for i in range(norder):
        output.append(str(source2[i]))
    output.append(random.choice(list(master_dict[1].keys()))[0])
    for i in range(output_length - (norder + 1)):
        try:
            append_next_value(master_dict, output, norder)
        except IndexError:
            # If the markov chain gets a token that has always been the end of an entry it will end here
            break
    return join_char.join(output)
