
"""File containing utility functions for XPath generation and manipulation
"""

import lxml
from bs4 import BeautifulSoup


def generate_abs_xpath(element):
    """Generate the full absolute XPath of an element
    """

    levels = []

    while element is not None:
        level_dict = {
            'name': element.tag,
            'position': None,
            'attributes': []
        }

        attrs = element.items()

        for pred in ["class", "id"]:
            if pred in element.keys():
                level_dict['attributes'].append(pred + "=\"" + element.get(pred) + "\"")

        level_dict['position'] = get_correct_position(level_dict, element)
        levels.append(level_dict_to_string(level_dict))
        element = element.getparent()

    levels.reverse()
    return generate_xpath(levels)


def uniform_quote(xpath):
    """Parsing function that changes all ' to "
    """

    return xpath.replace("'", "\"")


def parse_xpath(xpath):
    """Parse the XPath to return a list of levels

    Complementary to generate_xpath()
    """

    if xpath[1] == '/':
        xpath = xpath[1:]
    return xpath.split('/')[1:]


def generate_xpath(levels):
    """Generate an XPath given a list of levels

    Complementary to parse_xpath()
    """
    return '//'+'/'.join(levels)


def get_xpath_length(xpath):
    """Return the length of an XPath
    """

    return len(parse_xpath(xpath))


def get_top_element(xpath, target_element):
    """Return an element class corresponding to the target element's top level
    """

    length = get_xpath_length(xpath)
    element = target_element

    for i in range(1, length):
        element = element.getparent()

    return element


def get_correct_position(level_dict, element):
    """Get position with respect to its parent
    """

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
    """Check if dictionary form matches element
    """

    if (level_dict['name'] is not '*') and (level_dict['name'] != element.tag):
        return False

    if element.tag is lxml.etree.Comment:
        return False

    for attr in level_dict['attributes']:
        tmp = attr.split('=')
        key = tmp[0]
        value = tmp[1].split("\"")[1]

        if key not in element.keys() or element.get(key) != value:
            return False

    return True


def has_attribute(key, level_dict):
    """Check if dictionary form has an element
    """

    for attr in level_dict['attributes']:
        if attr.startswith(key):
            return True

    return False


def level_string_to_dict(level_string):
    """Convert an XPath string to dictionary form

    Complementary to level_dict_to_string()
    """

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
            preds = list(map(lambda x: x.strip(), s.split(' and ')))

            for pred in preds:
                if pred.startswith('@'):
                    dic['attributes'].append(pred[1:])

    return dic


def level_dict_to_string(level_dict):
    """Convert an XPath dictionary form to a string

    Complementary to level_string_to_dict()
    """

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


def cleanup(dom_filepath):
    """Handle inconsistencies in the HTML file
    """

    new_filepath = ""

    with open(dom_filepath, "r", encoding="utf-8") as str:
        soup = BeautifulSoup(str, features= "lxml")
        soup = soup.prettify()
        new_filepath = dom_filepath[:-5]+"_clean.html"

        with open(new_filepath, "w" , encoding="utf-8") as new:
            new.write(soup)

    return new_filepath
