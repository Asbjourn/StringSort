#!/usr/bin/python
import sys
import unittest


def process_string(trie, string, index, char_order, num_chars):
    """
    Processes a string to update a pseudo-trie
    
    No return, but updates the trie

    @type trie array
    @param trie An array represeting the current trie to be updated
    @type string string
    @param string The current string being processed
    @type index int
    @param index The current index in string to process
    @type char_order dict
    @param char_order A mapping [char:int] of chars to their lexicographic order
    @type num_chars int
    @param num_chars The number of distinct chars
    """
    if index >= len(string):
        trie[num_chars] = True
        return

    next_char = string[index]
    if trie[char_order[next_char]] == None:
        new_trie = [None] * (num_chars + 1)
        new_trie[num_chars] = False
        trie[char_order[next_char]] = new_trie

    index += 1
    process_string(trie[char_order[next_char]], string, index, char_order, num_chars)

def create_strings(trie, string, order_char, num_chars, word_count):
    """
    Processes a trie to create the sorted array of strings
    
    Returns the sorted array

    @type trie array
    @param trie An array represeting the current trie to be updated
    @type string string
    @param string The current string being constructed
    @type order_char dict
    @param order_char A mapping [int:char] of lexicographic order to the char
    @type num_chars int
    @param num_chars The number of distinct chars
    """
    strings = []
    if trie[num_chars]:
        for k in range(0, word_count[string]):
            strings.append(string)
    for i in range(0, num_chars):
        if trie[i] != None:
            new_string = string + order_char[i]
            new_strings = create_strings(trie[i], new_string, order_char, num_chars, word_count)
            for s in new_strings:
                strings.append(s)
    return strings
                

def sort_strings(strings, chars):
    """
    Sorts an array of string given a lexicographic order
    
    Returns the sorted array

    @type strings array
    @param strings An array of the strings to be sorted
    @type chars string
    @param chars A string containing all chars in lexicographic order
    """
    word_count = {}
    char_order = {}
    order_char = {}
    num_chars = 0

    # Build char heirarchy
    num_chars = len(chars)
    for i in range(0, num_chars):
        char_order[chars[i]] = i
        order_char[i] = chars[i]
        
    trie = [None] * (num_chars + 1)
    trie[num_chars] = False;
    for string in strings:
        # Build word occurence tally
        # Process only if not seen before
        if string not in word_count:
            word_count[string] = 0
            process_string(trie, string, 0, char_order, num_chars)
        word_count[string] += 1
        

    sorted = create_strings(trie, "", order_char, num_chars, word_count)

    return sorted

def main(argv):
    """
    Given n words, average m length, k lexicographic chars

    SPACE: O(k * n * m) -> O(n * m)
    The constructed trie creates an array of length k for each character in each word.
    Presumably n * m >> k and is the determining factor, yielding O(n * m) 

    RUNTIME: O((k + 2) * n * m + k) -> O(n * m)
    Each word is processed in the creation of the word count dict
    O(n * m)
    Each character in the lexicographical string is processed once
    O(k)
    Each character in each word is processed once in the creation of the trie
    O(n * m)
    During the recreation step, each of the k elements for each character in each words is visited,
    O(k * n * m)
    Presumably n * m >> k and is the determining factor, yielding O(n * m) 
    """
    print("Sorting: {0}, {1}".format(["acb", "dad", "abc", "bca", "bca"], "abcd"))
    print("{0}\n".format(sort_strings(["acb", "dad", "abc", "bca", "bca"], "abcd")))
    print("Sorting: {0}, {1}".format(["acb", "abc", "bca"], "cba"))
    print("{0}\n".format(sort_strings(["acb", "abc", "bca"], "cba")))
    print("Sorting: {0}, {1}".format(["aaa","", "aa",""], "a"))
    print("{0}\n".format(sort_strings(["aaa","", "aa",""], "a")))
    
if __name__ == "__main__":
    main(sys.argv[1:])
