def has_cents(price, comma_location):
    return set(price[comma_location + 1:]) == {'0'}


def round_price(price):
    # gets a string like $3.743,67 and return the int 3743 (will round the cents)
    comma_location = price.find(',')

    if comma_location == -1:
        # no cents
        price = price.replace('$', '')
        price = price.replace('.', '')
        return int(price)

    # extract what is after the comma
    # validate if centes are zero
    amount_to_increase = 0
    if has_cents(price, comma_location):
        amount_to_increase = 1

    # has cents then remove everything after the comma (including the comma)
    price = price[:comma_location]
    price = price.replace('$', '')
    price = price.replace('.', '')
    return int(price) + amount_to_increase
