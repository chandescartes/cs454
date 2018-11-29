import lxml

def uniform_quote(xpath):
    return xpath.replace("'", "\"")

# parse xpath return list of levels
def parse_xpath(xpath):
    if xpath[1] == '/':
        xpath = xpath[1:]
    return xpath.split('/')[1:]

# return legnth of xpath
def get_xpath_length(xpath):
    return len(parse_xpath(xpath))

# generate xpath from list of levels
def generate_xpath(levels):
    return '//'+'/'.join(levels)

# return element class of xpath top level
def get_top_element(xpath, target_element):
    length = get_xpath_length(xpath)
    element = target_element
    for i in range(1, length):
        element = element.getparent()
    return element

def has_attribute(key, level_dict):
    for attr in level_dict['attributes']:
        if attr.startswith(key):
            return True
    return False

def level_string_to_dict(level_string):
    dic = {
        'name': None,
        'position': None,
        'attributes': [],
        'text': None
    }
    s = level_string
    tmp = s.split('[')
    dic['name'] = tmp[0]

    for i in tmp[1:]:
        s = i.split(']')[0]
        if s.isdigit():
            dic['position'] = int(s)
        else:
            preds = list(map(lambda x: x.strip(), s.split('and')))
            for pred in preds:
                if pred.startswith('text()='):
                    dic['text'] = pred.split('\"')[1]
                elif pred.startswith('@'):
                    dic['attributes'].append(pred[1:])
    return dic

def level_dict_to_string(level_dict):
    dic = level_dict
    s = ""
    s = s + dic['name']
    if len(dic['attributes']) > 0 or dic['text'] is not None:
        preds = ""
        if dic['text'] is not None:
            preds = preds + "text()=\"" + dic['text'] + "\""
        for attr in dic['attributes']:
            if preds != "":
                preds = preds + " and "
            preds = preds + "@" +attr
        preds = '[' + preds + ']'
        s = s + preds
    if dic['position'] is not None:
        s = s + "[" + str(dic['position']) + "]"

    return s
