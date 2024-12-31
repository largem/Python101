
def combine_camel_words(input_string):
    # Split the input string into words
    words = input_string.split()
    
    # Convert each word to camel case
    camel_words = []
    for word in words:
        word = word.lower()
        camel_word = word[0].upper() + word[1:]
        camel_words.append(camel_word)
    
    # Join all words with underscore
    return "_".join(camel_words)