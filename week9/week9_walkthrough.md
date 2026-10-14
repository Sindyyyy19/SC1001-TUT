# Week 9 – Functions: 1A2B (Bulls & Cows), step by step

Full code: [bulls_and_cows.py](bulls_and_cows.py). Run it with `python bulls_and_cows.py`.

---

## Discussion 1 – Steps and flow (pseudocode)

What has to happen in one game:

1. Pick 4 different random digits as the target.
2. Set attempts = 0.
3. Ask the player for 4 digits. If the input is not 4 different digits, ask again.
4. Add 1 to attempts.
5. Compare guess with target and count bulls (A) and cows (B).
6. If bulls is 4, print "You Win!!" and the attempts, then stop.
7. Otherwise print "x A (Bulls) y B (Cows)" and go back to step 3.

```
START
  target <- 4 different random digits
  attempts <- 0
  REPEAT
      guess <- read input
      WHILE guess is not 4 different digits
          print error, guess <- read input
      attempts <- attempts + 1
      bulls, cows <- compare(target, guess)
      IF bulls != 4 THEN print bulls, cows
  UNTIL bulls == 4
  print "You Win!!", attempts
END
```

Flowchart in words: Start → Generate target → Get guess → (valid? no → back to Get guess) → Count A/B → (bulls == 4? no → Show result → back to Get guess; yes → Print win + attempts) → End.

---

## Discussion 2 – Function prototypes

Each step above becomes one function.

| Function | What it does | Parameters | Returns |
|---|---|---|---|
| `generate_target()` | Picks 4 different random digits | none | `str`, e.g. `"2468"` |
| `is_valid_guess(guess)` | Checks input is exactly 4 different digits | `guess` (str) | `bool` |
| `get_guess()` | Keeps asking until input is valid | none | `str` |
| `count_bulls_cows(target, guess)` | Counts A and B | `target` (str), `guess` (str) | `tuple` `(bulls, cows)` |
| `show_result(bulls, cows)` | Prints one round's result | `bulls`, `cows` (int) | `None` |
| `play_game()` | Runs the whole game | none | `int`, number of attempts |

Why store the number as a **string** and not an int? Because `0536` as an int becomes `536` and loses the leading 0, and a string lets us index each digit with `target[i]`.

---

## Discussion 3 – Implement each function

### Step 1: `generate_target()`

```python
import random

def generate_target():
    digits = random.sample("0123456789", 4)
    return "".join(digits)
```

- `random.sample(seq, 4)` picks 4 items from `seq` **without repeats**, so the digits are guaranteed different. Example result: `['2', '4', '6', '8']`.
- `"".join(...)` glues the list into one string: `"2468"`.

### Step 2: `is_valid_guess(guess)`

```python
def is_valid_guess(guess):
    if len(guess) != 4:
        return False
    if not guess.isdigit():
        return False
    if len(set(guess)) != 4:
        return False
    return True
```

Three checks, any failure returns `False` straight away:
- `len(guess) != 4` rejects `"123"` or `"12345"`.
- `guess.isdigit()` is `True` only if every character is 0–9, so `"12a4"` fails.
- `set(guess)` removes duplicates: `set("1123")` is `{'1','2','3'}`, length 3, so repeated digits fail.

### Step 3: `get_guess()`

```python
def get_guess():
    guess = input("Please input 4 digits: ")
    while not is_valid_guess(guess):
        print("Invalid! Enter 4 different digits, e.g. 1234.")
        guess = input("Please input 4 digits: ")
    return guess
```

- Read once, then loop **while** the input is invalid. The loop only exits once a valid guess is typed.
- Notice this function *calls* `is_valid_guess`. Functions can use other functions.

### Step 4: `count_bulls_cows(target, guess)` (the core logic)

```python
def count_bulls_cows(target, guess):
    bulls = 0
    cows = 0
    for i in range(4):
        if guess[i] == target[i]:
            bulls += 1
        elif guess[i] in target:
            cows += 1
    return bulls, cows
```

Go through positions 0, 1, 2, 3. For each digit of the guess:
- Same digit in the **same position** → bull.
- Otherwise, if the digit is **anywhere** in the target → cow. (`elif` matters: a bull must not also be counted as a cow.)

Trace with target `2468`, guess `1234`:

| i | guess[i] | target[i] | same? | in target? | result |
|---|---|---|---|---|---|
| 0 | 1 | 2 | no | no | – |
| 1 | 2 | 4 | no | yes | cow |
| 2 | 3 | 6 | no | no | – |
| 3 | 4 | 8 | no | yes | cow |

→ `(0, 2)`, i.e. 0A2B, matching the sheet. Guess `2478` gives `(3, 0)` = 3A.

`return bulls, cows` returns **two values** as a tuple; the caller unpacks it with `bulls, cows = count_bulls_cows(...)`.

### Step 5: `show_result(bulls, cows)`

```python
def show_result(bulls, cows):
    print(bulls, "A (Bulls)", cows, "B (Cows)")
```

Only prints, so it returns nothing (`None`). Output looks like `1 A (Bulls) 0 B (Cows)`.

---

## Discussion 4 – Combine everything

```python
def play_game():
    target = generate_target()
    attempts = 0
    bulls = 0
    while bulls != 4:
        guess = get_guess()
        attempts += 1
        bulls, cows = count_bulls_cows(target, guess)
        if bulls != 4:
            show_result(bulls, cows)
    print("You Win!!")
    print("Attempts:", attempts)
    return attempts

play_game()
```

Step by step:
1. Make the secret target once, before the loop.
2. Start `attempts` at 0 and `bulls` at 0 (so the `while` condition is true the first time).
3. Each round: get a valid guess, count one attempt, compare.
4. If not 4 bulls yet, show the A/B result and loop again.
5. When `bulls == 4`, the loop ends and we print the win message and attempts.
6. The last line `play_game()` actually starts the game. Defining a function does nothing until it is called.

Sample run (target was `0536`), same as the sheet's screenshot:

```
Please input 4 digits: 1234
1 A (Bulls) 0 B (Cows)
Please input 4 digits: 5678
0 A (Bulls) 2 B (Cows)
Please input 4 digits: 7890
0 A (Bulls) 1 B (Cows)
Please input 4 digits: 1569
1 A (Bulls) 1 B (Cows)
Please input 4 digits: 0536
You Win!!
Attempts: 5
```

**Tip for testing:** add `print(target)` right after `target = generate_target()` so you can see the answer while debugging, then remove it.

---

## Key ideas about functions this tutorial practises

- **One job per function**: each step of the algorithm is its own small function, which makes it easy to test alone.
- **Parameters** carry data in (`target`, `guess`); **return values** carry results out (`bulls, cows`).
- **Returning multiple values** as a tuple and unpacking them.
- **Functions calling functions**: `play_game` → `get_guess` → `is_valid_guess`.
- **Local variables**: `bulls` inside `count_bulls_cows` is separate from `bulls` inside `play_game`; data moves between them only through return values.
