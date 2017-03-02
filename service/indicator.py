from collections import defaultdict

class Indicator():
    def indicate(self, guess, answer):
        if(len(guess) != len(answer)):
            raise InvalidInput("Length of answer and guess are different.")

        aligned = 0;
        not_aligned = 0;

        chars_guess = defaultdict(int)
        chars_answer = defaultdict(int)

        for i in range(len(guess)):
            char_guess = guess[i:i+1]
            char_answer = answer[i:i+1]

            if char_guess == char_answer:
                aligned += 1
            else: 
                chars_guess[char_guess] += 1
                chars_answer[char_answer] += 1

        for key, value in chars_guess.iteritems():
            if chars_answer.get(key):
                not_aligned += min(value, chars_answer.get(key))

        return aligned, not_aligned
