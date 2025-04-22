from collections import defaultdict

# Sample grammar productions as a list of strings
productions = [
    "E -> T E'",
    "E' -> + T E' | e",
    "T -> F T'",
    "T' -> * F T' | e",
    "F -> ( E ) | id"
]

# Step 1: Parse grammar into a dictionary
grammar = defaultdict(list)

for prod in productions:
    head, body = prod.split("->")
    head = head.strip()
    alternatives = body.strip().split("|")
    for alt in alternatives:
        grammar[head].append(alt.strip())

# Step 2: Define FIRST set storage
first = defaultdict(set)

# Step 3: Utility to check if a symbol is terminal
def is_terminal(symbol):
    return not symbol.isupper() and symbol != 'e'

# Step 4: Compute FIRST set for a symbol
def compute_first(symbol):
    if is_terminal(symbol) or symbol == 'e':
        return {symbol}

    if first[symbol]:  # Already computed
        return first[symbol]

    for production in grammar[symbol]:
        symbols = production.split()

        for sym in symbols:
            sym_first = compute_first(sym)
            first[symbol].update(sym_first - {'e'})

            if 'e' not in sym_first:
                break
        else:
            # All symbols had e, so include e in the FIRST set
            first[symbol].add('e')

    return first[symbol]

# Step 5: Compute FIRST sets for all non-terminals
for non_terminal in grammar:
    compute_first(non_terminal)

# Step 6: Display the FIRST sets
print("=== FIRST Sets ===")
for non_terminal, first_set in first.items():
    formatted = ', '.join(sorted(first_set))
    print(f"FIRST({non_terminal}) = {{ {formatted} }}")
