from constants import DATA_PATH

def load_high_score():
    try:
        with open(DATA_PATH, "r") as f:
            return int(f.read())
    except:
        return 0

def save_high_score(score):
    with open(DATA_PATH, "w") as f:
        f.write(str(score))
