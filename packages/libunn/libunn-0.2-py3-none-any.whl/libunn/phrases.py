# Part of libunn, view: https://github.com/juanvel4000/libunn
import random

phrases = [
'You will have many recoverable tape errors. ',
'Sacred cows make great hamburgers. ',
'The only winner in the War of 1812 was Tchaikovsky. 		-- David Gerrold ',
"What did ya do with your burden and your cross? Did you carry it yourself or did you cry? You and I know that a burden and a cross, Can only be carried on one man's back. 		-- Louden Wainwright III ",
'The older a man gets, the farther he had to walk to school as a boy. ',
'Keep emotionally active.  Cater to your favorite neurosis. ',
'Sanity and insanity overlap a fine grey line. ',
'Who was that masked man? ',
"I love dogs, but I hate Chihuahuas.  A Chihuahua isn't a dog.  It's a rat with a thyroid problem. ",
'If you do not wish a man to do a thing, you had better get him to talk about it; for the more men talk, the more likely they are to do nothing else. 		-- Carlyle '
]


def rand():
    if not phrases:
        return None
    random.shuffle(phrases)
    return random.choice(phrases)

def add(newphrase):
    global phrases
    if newphrase in phrases:
        return False
    phrases.append(newphrase)
    return True

def rm(phrase):
    global phrases
    if phrase not in phrases:
        return False
    phrases.remove(phrase)
    return True
def check(phrase):
    global phrases
    if phrase not in phrases:
        return False
    else:
        return True
