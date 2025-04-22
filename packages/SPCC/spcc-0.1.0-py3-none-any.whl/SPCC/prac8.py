from collections import defaultdict

# Sample grammar productions
productions = [

    "E -> T E'",
    "E' -> + T E' | e",
    "T -> F T'",
    "T' -> * F T' | e",
    "F -> ( E ) | id"
]


# Step 1: Parse the grammar
grammar = defaultdict(list)
non_terminals = set()
terminals = set()

for prod in productions:
    head, body = prod.split("->")
    head = head.strip()
    non_terminals.add(head)
    alternatives = body.strip().split("|")
    for alt in alternatives:
        grammar[head].append(alt.strip())

# Step 2: Helper functions
def is_terminal(symbol):
    return not symbol.isupper() and symbol != 'e'

first = defaultdict(set)
follow = defaultdict(set)

# Step 3: Compute FIRST sets
def compute_first(symbol):
    if is_terminal(symbol):
        return {symbol}
    if symbol == 'e':
        return {'e'}
    if first[symbol]:  # already computed
        return first[symbol]

    for production in grammar[symbol]:
        symbols = production.split()
        for sym in symbols:
            sym_first = compute_first(sym)
            first[symbol].update(sym_first - {'e'})
            if 'e' not in sym_first:
                break
        else:
            first[symbol].add('e')
    return first[symbol]

# Step 4: Compute FIRST of a string of symbols
def compute_first_of_string(symbols):
    result = set()
    for sym in symbols:
        sym_first = compute_first(sym)
        result.update(sym_first - {'e'})
        if 'e' not in sym_first:
            break
    else:
        result.add('e')
    return result

# Step 5: Compute FOLLOW sets
def compute_follow():
    start_symbol = list(grammar.keys())[0]
    follow[start_symbol].add('$')  # $ denotes end of input

    changed = True
    while changed:
        changed = False
        for head in grammar:
            for production in grammar[head]:
                symbols = production.split()
                for i, symbol in enumerate(symbols):
                    if symbol in non_terminals:
                        next_symbols = symbols[i + 1:]
                        next_first = compute_first_of_string(next_symbols)
                        before = len(follow[symbol])
                        follow[symbol].update(next_first - {'e'})
                        if 'e' in next_first or not next_symbols:
                            follow[symbol].update(follow[head])
                        if len(follow[symbol]) > before:
                            changed = True

# Step 6: Compute all FIRST and FOLLOW sets
for non_terminal in grammar:
    compute_first(non_terminal)
compute_follow()

# Step 7: Display the FOLLOW sets
print("=== FOLLOW Sets ===")
for non_terminal, follow_set in follow.items():
    formatted = ', '.join(sorted(follow_set))
    print(f"FOLLOW({non_terminal}) = {{ {formatted} }}")
