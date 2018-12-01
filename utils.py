import lxml

def generate_abs_path(element):
    levels = []

    while element is not None:
        level_dict = {
            'name': element.tag,
            'position': None,
            'attributes': []
        }

        attrs = element.items()
        for pred in ["class", "id"]: # FIXME add other attributes?
            if pred in element.keys():
                level_dict['attributes'].append(pred + "=\"" + element.get(pred) + "\"")

        level_dict['position'] = get_correct_position(level_dict, element)

        levels.append(level_dict_to_string(level_dict))
        element = element.getparent()

    levels.reverse()
    return generate_xpath(levels)

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

def get_correct_position(level_dict, element):
    position = 1
    if element.getparent() is None:
        return position
    else:
        siblings = element.getparent()
        matching_siblings = []
        for sibling in siblings:
            if is_element_matching_level(sibling, level_dict):
                matching_siblings.append(sibling)
        for i, sibling in enumerate(matching_siblings):
            if sibling == element:
                return position + i
    print("ERROR: failed getting correct position")
    return position

def is_element_matching_level(element, level_dict):
    if level_dict['name'] is not '*' and level_dict['name'] != element.tag:
        return False
    for attr in level_dict['attributes']:
        tmp = attr.split('=')
        key = tmp[0]
        value = tmp[1].split("\"")[1]
        if key not in element.keys() or element.get(key) != value:
            return False
    return True


def has_attribute(key, level_dict):
    for attr in level_dict['attributes']:
        if attr.startswith(key):
            return True
    return False

def level_string_to_dict(level_string):
    dic = {
        'name': None,
        'position': None,
        'attributes': []
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
                if pred.startswith('@'):
                    dic['attributes'].append(pred[1:])
    return dic

def level_dict_to_string(level_dict):
    dic = level_dict
    s = ""
    s = s + dic['name']
    if len(dic['attributes']) > 0:
        preds = ""
        for attr in dic['attributes']:
            if preds != "":
                preds = preds + " and "
            preds = preds + "@" +attr
        preds = '[' + preds + ']'
        s = s + preds
    if dic['position'] is not None:
        s = s + "[" + str(dic['position']) + "]"
    return s
