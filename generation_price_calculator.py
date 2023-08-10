def get_tokens(string):
    count = len(string)
    return count / 4


def read_file(file_path):
    with open(file_path, 'r') as file:
        contents = file.read()
    return contents


def calculate_token_price(tokens: float):
    print(f"\n The generation contains {tokens} tokens")
    return tokens * 0.002 / 1000


def calculate_generation_price(string):
    return calculate_token_price(get_tokens(string))


def calculate_generation_price_of_file(file_path):
    string = read_file(file_path)
    return calculate_token_price(get_tokens(string))


price = calculate_generation_price_of_file('LocalFiles/bussiness_plan.txt')
print(f"\n\n This generation will cost approximately ${price}")
