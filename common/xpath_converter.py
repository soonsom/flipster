import os

from utils.filehandlers import load_json


def get_aid(json_dict):
    json_data = load_json(os.path.abspath(f'./resources/aid_{os.environ["PLATFORM"]}.json'))
    return json_data[json_dict]


def get_value(json_dict):
    json_data = load_json(os.path.abspath('./resources/strings.json'))
    return json_data[json_dict]


def get_xpath_by_name(value, ios_attr_type="name", android_attr_type="text"):
    # ios_attr_type: name, value, label
    # android_attr_type: text, content-desc, resource-id
    attr_type = {
        "ios": ios_attr_type,
        "android": android_attr_type
    }
    return f'//*[@{attr_type[os.environ["PLATFORM"]]}="{get_value( value)}"]'


def get_xpath_by_direct_value(value, ios_attr_type="name", android_attr_type="text"):
    # ios_attr_type: name, value, label
    # android_attr_type: text, content-desc, resource-id
    attr_type = {
        "ios": ios_attr_type,
        "android": android_attr_type
    }
    return f'//*[@{attr_type[os.environ["PLATFORM"]]}="{value}"]'


def get_xpath_contains(text, ios_attr_type="name", android_attr_type="text"):
    # ios_attr_type: name, value, label
    # android_attr_type: text, content-desc, resource-id
    attr_type = {
        "ios": ios_attr_type,
        "android": android_attr_type
    }
    return f'//*[contains(@{attr_type[os.environ["PLATFORM"]]}, "{get_value(text)}")]'


def get_xpath_contains_by_value(value, ios_attr_type="name", android_attr_type="text"):
    # ios_attr_type: name, value, label
    # android_attr_type: text, content-desc, resource-id
    attr_type = {
        "ios": ios_attr_type,
        "android": android_attr_type
    }
    return f'//*[contains(@{attr_type[os.environ["PLATFORM"]]}, "{value}")]'
