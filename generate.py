import pickle
import random

def load():
    with open('my_prob.pkl', 'rb') as f:
        return pickle.load(f)


def main():
    prob = load()
    print 'Files are present: executing...'
    max_length = 0
    for key in prob:
        if len(key) > max_length:
            max_length = len(key)
    sentence = []

    while True:
        words = random.choice(prob.keys())
        if len(words) == max_length and '</s>' not in words and '<s>' not in words:
            for word in words:
                sentence.append(word)
            break

    while len(sentence) < 10:

        flag = True
        i = 1
        while flag and i < max_length:
            max_prob = 0.0
            max_key = []
            if i < max_length-1:
                last = sentence[-(max_length-i):]
                for key in prob:
                    if len(key) == ((max_length-i)+1):
                        flag2 = True
                        for j in range(max_length-i):
                            if key[j] <> last[j]:
                                flag2 = False
                        if key[-1] == '</s>':
                            flag2 = False
                        if flag2:
                            if max_prob < prob[key]:
                                max_prob = prob[key]
                                max_key = list(key)
                i += 1
                if max_prob > 0:
                    flag  = False
                    break

            else:
                flag3 = True
                while flag3:
                    words = random.choice(prob.keys())
                    if len(words) == 1 and '</s>' not in words and '<s>' not in words:
                        max_key = list(words)
                        max_prob = prob[words]
                        flag3 = False
                        flag = False

        # print ma  x_key
        if len(max_key) > 1:
            sentence.append(max_key[-1])
        else:
            sentence.append(max_key[0])
    print ' '.join(sentence)

main()
