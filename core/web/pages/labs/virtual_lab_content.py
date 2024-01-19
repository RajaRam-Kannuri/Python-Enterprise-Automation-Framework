from selene import Collection, Element, browser, have

from core.web.elements.base_element import BaseElement
from core.web.pages.labs.lab_pages import SingleVLPage
from util.web.assist.allure import report
from util.web.assist.selene.extended import by


class ContentVLPage(SingleVLPage):
    def __init__(self):
        super().__init__()
        self.content_section = browser.element('//article[@class="tab-content-wrapper"]')
        self.add_task_button = self.content_section.element("button.add-task-button")
        self.add_criteria_button = self.content_section.element("button.add-criteria-button")
        self.add_action_button = self.content_section.element("button.add-action-button")
        self.task = TaskVL(root=browser.element('//*[@class[contains(., "main-wrapper drag-and-drop-item")]]'))
        self.tasks = self.content_section.all(".//article//header")
        self.variables_dropdown_list: Collection = browser.all(
            by.class_starts_with("VariablesSelectorList-module_item_")
        )
        self.criteria_list: Collection = self.content_section.all(".acceptance-criteria-item-wrapper")
        self.actions_list: Collection = self.content_section.all(".action-item-wrapper")
        self.remove_criteria_button = self.content_section.element("button.remove-criteria-button")
        self.remove_action_button = self.content_section.element(".remove-action-button")
        self.edit_criteria_button = self.content_section.element(".edit-criteria-button")
        self.edit_action_button = self.content_section.element(".edit-action-button")


class TaskVL(BaseElement):
    def __init__(self, root):
        super().__init__()
        self._container: Element = root
        self.remove_step_button = self._container.element(by.class_contains("remove-step-button"))
        self.remove_task_button = self._container.element(by.class_contains("remove-task-button"))
        self.hints = browser.all(by.class_name("hint-wrapper"))
        self.steps = browser.all('.//article//*[@class="main-wrapper"]')
        self.expand_task_button = self._container.element('.//*[@class="summary"]')
        self.step_description_input = self._container.element("article.wrapper .ProseMirror p")
        self.task_description_input = self._container.element('.//*[@class="content-wrapper"]//p')
        self.task_name_input = self._container.element('.//*[@role="textbox"]')
        self.hint_name_input = self._container.element('.//*[@class="hint-wrapper"]//p')
        self.task_name_translation_status = self._container.element(
            './/*[@role="textbox"]/following::*[@class[contains(., "TranslationStatus")]]'
        )
        self.task_description_translation_status = self._container.element(
            './/*[@class="content-wrapper"]//following::*[@class[contains(., "TranslationStatus")]]'
        )
        self.step_description_translation_status = self._container.element(
            './/*[@class="wrapper"]//following::*[@class[contains(., "TranslationStatus")]]'
        )
        self.hint_name_translation_status = self._container.element(
            './/*[@class="hint-wrapper"]//*[@class[contains(., "TranslationStatus")]]'
        )
        self.translate_button = self._container.element('.//button[text()="Translate"]')
        self.approve_translation_button = self._container.element('.//button[text()="Approve"]')

    @report.step
    def check_task_scope_statuses(self, expected_status: str):
        self.task_name_translation_status.should(have.exact_text(expected_status))
        self.task_description_translation_status.should(have.exact_text(expected_status))
        self.step_description_translation_status.should(have.exact_text(expected_status))
        self.hint_name_translation_status.should(have.exact_text(expected_status))

    @report.step
    def renew_vl_content(self, new_content: str):
        self.task_description_input.click().clear().type(new_content)
        self.task_name_input.click().clear().type(new_content)
        self.step_description_input.click().clear().type(new_content)
        self.hint_name_input.click().clear().type(new_content)
        self.task_description_input.click()  # sometimes changes are not applied until you click smth else
