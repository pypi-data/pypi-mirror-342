import re

def check_strength(password):
    return {
        'length': len(password) >= 8,
        'uppercase': bool(re.search(r'[A-Z]', password)),
        'number': bool(re.search(r'\d', password)),
        'special': bool(re.search(r'[^A-Za-z0-9]', password)),
        'score': sum([
            len(password) >= 8,
            bool(re.search(r'[A-Z]', password)),
            bool(re.search(r'\d', password)),
            bool(re.search(r'[^A-Za-z0-9]', password)),
        ])
    }
