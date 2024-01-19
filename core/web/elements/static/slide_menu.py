from selene.core.entity import Element
from selene.support.shared import browser

from core.web.elements.base_element import BaseElement
from util.web.assist.selene.extended import by


class SlideMenu(BaseElement):
    root_locator = ".drawer-content-wrapper"

    def __init__(self):
        super().__init__()
        self._container: Element = browser.element(self.root_locator)
        self.controls_header = self._container.element(by.class_starts_with("Drawer-module_header"))
        self.close_window_button = self.controls_header.element(by.class_starts_with("Drawer-module_closeButton"))

        # content part
        self.content = self._container.element(by.class_starts_with("Drawer-module_contentWrapper"))
        self.name_field = self.content.element("h2")

    @staticmethod
    def _get_field_locator(name: str):
        """The method builds and returns a locator for a field in a slide menu.

        Args:
            name: the name of a label as it is displayed in a field. It's case-sensitive!

        Returns:
            prepared locator for a slide menu field

        """
        content_field_locator = (
            './/*[starts-with(@class,"CellItem_cellTitle") and text()="{field}"]/following-sibling::div'
        )
        return content_field_locator.format(field=name)
