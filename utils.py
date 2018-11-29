import lxml

def uniform_quote(xpath):
    return xpath.replace("'", "\"")

# parse xpath return list of levels
def parse_xpath(xpath):
    if xpath[1] == '/':
        xpath = xpath[1:]
    return xpath.split('/')[1:]

# return legnth of xpath
def get_xpath_legnth(xpath):
    return len(parse_xpath(xpath))

# generate xpath from list of levels
def generate_xpath(levels):
    return '//'+'/'.join(levels)

# return element class of xpath top level
def get_top_element(xpath, target_element):
    length = get_xpath_legnth(xpath)
    element = target_element
    for i in range(1, length):
        element = element.getparent()
    return element

def parse_level(level):

    res = {
        'name': None,
        'position': None,
        'attributes': [],
        'text': None
    }

    tmp = level.split('[')
    res['name'] = tmp[0]

    for i in tmp[1:]:
        s = i.split(']')[0]
        if s.isdigit():
            res['position'] = int(s)
        else:
            preds = list(map(lambda x: x.strip(), s.split('and')))
            for pred in preds:
                if pred.startswith('text()='):
                    res['text'] = pred.split('\"')[1]
                elif pred.startswith('@'):
                    res['attributes'].append(pred[1:])
    return res
