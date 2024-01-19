from selene import Element, be, by, have

from core.web.elements.base_element import BaseElement
from core.web.elements.dynamic.more_menu import BaseMenu
from core.web.elements.static.modal import Modal
from core.web.pages.base_page import BasePage, StaticUrlPage
from settings import settings
from util.web.assist.allure import report


class BaseElementWithRoot(BaseElement):
    def __init__(self, root: Element):
        super().__init__()
        self._container = root

    @report.step
    def should_be_visible(self):
        self._container.should(be.visible)


class TextEditor(BaseElementWithRoot):
    def __init__(self, root: Element):
        super().__init__(root=root)
        self.title = self._container.element("h6")
        self.input = self._container.element("div.tiptap")


class ScenePreviewContextMenu(BaseMenu):
    def __init__(self, root: Element):
        super().__init__(
            root=root,
            open_menu_button_locator="[data-testid=scene-context-menu-toggle-button]",
            opened_menu_locator='//*[@data-testid="scene-context-menu"]',
            item_locator='//li[@role="menuitemcheckbox"]',
        )
        self.duplicate_item = self._container.element('//*[@data-testid="clone-scene"]')
        self.delete_item = self._container.element('//*[@data-testid="delete-scene"]')


class ScenePreviewButton(BaseElementWithRoot):
    selected_condition = have.css_property("selected")

    def __init__(self, root: Element):
        super().__init__(root=root)

        self.context_menu = ScenePreviewContextMenu(root=root)

    @report.step
    def duplicate(self):
        self._container.hover()
        self.context_menu.make_opened()
        self.context_menu.duplicate_item.click()

    @report.step
    def delete(self):
        self._container.hover()
        self.context_menu.make_opened()
        self.context_menu.delete_item.click()

    def click(self):
        self._container.click()

    @report.step
    def should_be_active(self):
        self._container.should(self.selected_condition)


class SceneDeleteModal(Modal):
    def __init__(self):
        super().__init__()
        self.ok_button = self.footer.element(by.text("OK"))
        self.cancel_button = self.footer.element(by.text("Cancel"))


class ScenesPanel(BaseElementWithRoot):
    scene_preview_testid = "scene-preview"

    def __init__(self, root: Element):
        super().__init__(root=root)
        self.scenes = self._container.all(f"span:has([data-testid^={self.scene_preview_testid}])")
        self.new_scene_button = self._container.element("[data-testid=add-new-scene-button]")

    @report.step
    def get_scene_by_index(self, index: int) -> ScenePreviewButton:
        return (
            ScenePreviewButton(
                self._container.element(f"span:has([data-testid={self.scene_preview_testid}-{index+1}])")
            )
            .as_(f"scene#{index + 1}")
            .set_previous_name_chain_element(self)
        )

    @report.step
    def get_active_scene(self) -> ScenePreviewButton:
        return (
            ScenePreviewButton(self.scenes.element_by(ScenePreviewButton.selected_condition))
            .as_("active_scene")
            .set_previous_name_chain_element(self)
        )

    @report.step
    def create_scene(self):
        scenes_count = len(self.scenes)
        self.new_scene_button.click()
        self.scenes.should(have.size(scenes_count + 1))

    @report.step
    def create_scenes(self, count: int):
        for _ in range(count):
            self.create_scene()


class ControlsBar(BaseElementWithRoot):
    def __init__(self, root: Element):
        super().__init__(root=root)
        self.avatars_button = self._container.element("[data-testid=toggle-avatar-inspector-button]")
        self.settings_button = self._container.element("[data-testid=project-settings-button]")
        self.toggle_avatar_inspector_button = self._container.element("[data-testid=toggle-inspector-button-wrapper]")


class InspectorPanel(BaseElementWithRoot):
    pass


class AvatarProjectBasePage(BasePage):
    def __init__(self):
        super().__init__()
        self.scenes_panel = ScenesPanel(root=self.browser.element("[data-testid=scenes-list]"))
        self.text_editor = TextEditor(root=self.browser.element("[class*=textEditor]"))
        self.controls_bar = ControlsBar(root=self.browser.element("[data-testid=top-bar-wrapper]"))
        self.inspector_panel = InspectorPanel(root=self.browser.element("[data-testid=desktop-inspector]"))
        self.delete_scene_modal = SceneDeleteModal()


class AvatarDemoPage(StaticUrlPage, AvatarProjectBasePage):
    def __init__(self):
        super().__init__(url=settings.base_url_avatar)
