from common.element_handlers import ElementHandler
from common.xpath_converter import get_aid, get_xpath_by_name, get_xpath_contains, get_xpath_by_direct_value
from utils.enums import Selector, XpathType


class HelperFunctions(ElementHandler):
    # 화면에 노출되지 않는 엘러멘트가 있다면 반환, 해당 함수 반환갑이 있는경우 raise AssertionError로 활용
    def get_els_not_shown(self,
                          els,
                          xpath_type=XpathType.AID,
                          ios_attr_type="name",
                          android_attr_type="text"):
        els_not_shown = []
        el_key = ""

        # xpath_converter에서 xpath를 받아오는 형태가 구분되어 있지만
        # element_handler에 있는 함수들은 Accessibility id, XPath로만 구분을 하기 때문에 xpath를 할당해줌
        selector = Selector.XPATH

        for el in els:
            if xpath_type == XpathType.AID:
                selector = Selector.AID
                el_key = get_aid(el)

            elif xpath_type == XpathType.DIRECT_AID:
                selector = Selector.AID
                el_key = el

            elif xpath_type == XpathType.XPATH:
                el_key = get_xpath_by_name(el,
                                           ios_attr_type=ios_attr_type,
                                           android_attr_type=android_attr_type)

            elif xpath_type == XpathType.CONTAINS:
                el_key = get_xpath_contains(el,
                                            ios_attr_type=ios_attr_type,
                                            android_attr_type=android_attr_type)

            elif xpath_type == XpathType.DIRECT_VALUE:
                el_key = get_xpath_by_direct_value(el,
                                                   ios_attr_type=ios_attr_type,
                                                   android_attr_type=android_attr_type)

            if not self.is_element_present(el_key, find_by=selector):
                els_not_shown.append(el)

        return els_not_shown
