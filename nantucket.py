import poetry
import argparse

parser = argparse.ArgumentParser(description='Find accidental limericks in any text.')
parser.add_argument('--text',
                   help='the file you want to search for limericks in, ie "ulysses.txt"')
args = parser.parse_args()

tokens = poetry.tokenize(args.text)


def overflows_line(syllable_counter, current_sylct):  # return true if the word would overflow the line
    if syllable_counter < 8 and current_sylct > 8 - syllable_counter:
        return True
    elif syllable_counter < 16 and current_sylct > 16 - syllable_counter:
        return True
    elif syllable_counter < 21 and current_sylct > 21 - syllable_counter:
        return True
    elif syllable_counter < 26 and current_sylct > 26 - syllable_counter:
        return True
    elif syllable_counter < 35 and current_sylct > 35 - syllable_counter:
        return True
    return False


limericks = []
word_data = {}
i = 0
while i < len(tokens):
    if tokens[i] == '':
        tokens.remove('')
        continue
    start_word = tokens[i]
    if not start_word in word_data:
        word_data[start_word] = {"sylct": poetry.nsyl(start_word),
        "phonemes": poetry.phonemes(start_word)}
        # Uses more space in exchange for getting more speed
    word_array = [start_word]
        # Holds the actual words of the potential limerick
    syllable_counter = word_data[start_word]['sylct']
    n = i + 1
    rhyme_scheme = {}  # Tracks the rhyme scheme
    while n < len(tokens):
        if tokens[n] == '':
            tokens.remove('')
            continue
        next_word = tokens[n]
        if not next_word in word_data:
            word_data[next_word] = {"sylct": poetry.nsyl(next_word),
            "phonemes": poetry.phonemes(next_word)}
        sylct = word_data[next_word]['sylct']
        if overflows_line(syllable_counter, sylct):
            break  # break out if a word overflows the line
        word_array.append(next_word)
        syllable_counter += sylct
        phonemes = word_data[next_word]['phonemes']
        if syllable_counter == 8:
            if not phonemes:
                break
            rhyme_scheme['A'] = phonemes
            word_array.append("\n")
        elif syllable_counter == 16:
            word_array.append("\n")
            if not phonemes:
                break
            if (not 'A' in rhyme_scheme or not \
                poetry.rhyme_from_phonemes(rhyme_scheme['A'], phonemes)):
                break
        elif syllable_counter == 21:
            if phonemes == rhyme_scheme['A'] or not phonemes:
                break
            rhyme_scheme['B'] = phonemes
            word_array.append("\n")
        elif syllable_counter == 26:
            word_array.append("\n")
            if not phonemes:
                break
            if (not 'B' in rhyme_scheme or not \
                poetry.rhyme_from_phonemes(rhyme_scheme['B'], phonemes)):
                break
        elif syllable_counter == 35:
            if not phonemes:
                break
            if poetry.rhyme_from_phonemes(rhyme_scheme['A'], phonemes):
                limericks.append(word_array)
            break
        n += 1
    i += 1

if limericks == []:
    print "Sorry, there were no limericks found in your text!"
else:
    for limerick in limericks:
        limerick = " ".join(limerick)
        print limerick
