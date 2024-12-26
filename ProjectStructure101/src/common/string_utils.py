def reverse_string(input_str):
    return input_str[::-1]

def capitalize_words(input_str):
    words = input_str.split()
    capitalized_words = [word.capitalize() for word in words]
    return ' '.join(capitalized_words)

def count_vowels(input_str):
    vowels = "aeiouAEIOU"
    return sum(1 for char in input_str if char in vowels)

def remove_whitespace(input_str):
    return ''.join(input_str.split())
