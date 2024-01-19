from util.web.assist.allure.chainable_naming import ChainableNamingElement


class BaseElement(ChainableNamingElement):
    def __str__(self):
        return self.description or self.__class__.__name__
