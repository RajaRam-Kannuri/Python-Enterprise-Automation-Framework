from core.web.elements.dynamic.form_control import TextFormControl


class VMTextFormControl(TextFormControl):
    by_label_locator_stub = './/*[@class[contains(., "FormControl-module")] and .//label[text()="{by_label}"]]'
