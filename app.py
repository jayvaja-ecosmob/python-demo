def count_vowels(file_path):

    vowels = "aeiouAEIOU"

    count = {
        "a":0,
        "e":0,
        "i":0,
        "o":0,
        "u":0
    }

    with open(file_path, "r") as file:
        content = file.read()

        for char in content:
            if char.lower() in count:
                count[char.lower()] += 1

    return count


file_name = "text.txt"

result = count_vowels(file_name)

print("Vowel Count:\n")

for vowel, value in result.items():
    print(vowel, ":", value)
