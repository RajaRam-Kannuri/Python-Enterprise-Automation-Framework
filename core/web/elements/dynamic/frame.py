from contextlib import contextmanager
from typing import Self

from selene.core.entity import Element
from selene.support.conditions import be
from selene.support.shared import browser

from core.web.elements.base_element import BaseElement


class Frame(BaseElement):
    """
    A common element for convenient iframe management.
    It stores elements that is located inside the iframe and provides a convenient way to switch to/from an iframe,
    using the contextmanager. It helps to track an active iframe by indenting.

    Here are two examples:

    ...interacting with elements outside the iframe...
    browser.switch_to.frame(page.iframe_on_page)
    page.some_element_inside_iframe.should(be.visible)
    page.another_element_inside_iframe.click()
    browser.switch_to.parent_frame()
    ...interacting with elements outside the iframe...

    Is the same as:

        ...interacting with elements outside the iframe...
        with page.frame.make_active() as frame:
                frame.some_element_inside_iframe.should(be.visible)   # the different indent levels help to distinguish
                frame.another_element_inside_iframe.click()           # where the current frame ends
        ...interacting with elements outside the iframe...


    Also, this element helps to wrap an arbitrary page in an iframe (as LMS developers like to do).

    For example, in Labs we have an independent PreviewLabPage, and the same page in LMS is wrapped in an iframe.
    To create a complex "page in iframe" element, simply use double inheritance:

        class VirtualLabContent(Frame, PreviewLabPage):    # the ordering of inheritance is important!
            def __init__(self):
            super().__init__(iframe=browser.element('iframe[id="tooliframe"]'))

    """

    def __init__(self, iframe: Element, *args, **kwargs):
        self.iframe = iframe
        self._container = browser.element("body")

        self.is_active = True
        super().__init__(*args, **kwargs)
        self.is_active = False

    @contextmanager
    def make_active(self) -> Self:
        try:
            self.iframe.should(be.visible)
            browser.switch_to.frame(self.iframe())
            self.is_active = True
            yield self
        finally:
            browser.switch_to.parent_frame()
            self.is_active = False
