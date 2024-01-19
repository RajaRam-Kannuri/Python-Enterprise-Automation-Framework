from functools import cached_property
from typing import Dict, Generic, Tuple, Type, TypeVar

import allure
from selene import be, have
from selene.core import query
from selene.core.entity import Collection, Element

from core.web.elements.base_element import BaseElement
from core.web.elements.dynamic.more_menu import MoreMenu, OldMoreMenu
from util.web.assist.allure import report
from util.web.assist.selene.extended import by

CSS = str
XPATH = str
CSS_or_XPATH = CSS | XPATH
R = TypeVar("R", bound="Row")
T = TypeVar("T", bound="Table[Row]")


class Row(BaseElement):
    def __init__(self, root: Element, cell_locators: Dict[str, CSS_or_XPATH]):
        """

        Args:
            root:
            cell_locators: dictionary with column_name: its_locator pairs.
        """
        super().__init__()
        self.cell_locators = cell_locators
        self._container = root
        self._values: dict = {}
        # alias for an element direct access
        self.body: Element = self._container

    @allure.step("Extracting data from the row")
    def _parse_values(self):
        for field_name, locator in self.cell_locators.items():
            self._container.element(locator).should(have._not_.exact_text(""))
            self._values[field_name] = self._container.element(locator).get(query.text)

    @property
    def values(self) -> dict:
        if not self._values:
            self._parse_values()
        return self._values

    def should_have_values(self, expected_row_values: dict):
        error_message = f"Row doesn't match!\n expected: {expected_row_values}\n presented: {self.values}"
        with allure.step(f'Check that row has expected values "{expected_row_values.items()}"'):
            assert expected_row_values.items() <= self.values.items(), error_message


class TableRowWithMenu(Row):
    def __init__(self, root: Element, cell_locators: dict):
        super().__init__(root, cell_locators)
        self.more_menu: MoreMenu = MoreMenu(self._container)


class TableRowWithOldMenu(Row):
    def __init__(self, root: Element, cell_locators: dict):
        super().__init__(root, cell_locators)
        self.more_menu: OldMoreMenu = OldMoreMenu(self._container)


class Table(BaseElement, Generic[R]):
    def __init__(
        self,
        root: Element,
        locators_dict: Dict[str, CSS_or_XPATH] | None,
        header_cell_locator: CSS_or_XPATH = "th",
        row_locator: CSS_or_XPATH = "tr",
        table_header_locator: CSS_or_XPATH = "thead",
        row_type: Type[R] = TableRowWithMenu,
    ):
        """Just a common table class with a variable type of row.

        Args:
            root: the element where to look for the table
            locators_dict: dictionary with pairs of column_name: its_locator.
            For example:
            locators_dict={"lab_provider": ".lab-provider", "lab_name": ".lab-title"}
            means that a row in your table has two columns "lab_provider" and "lab_name"
            with the locators ".lab-provider" and ".lab-title" respectively
             locators_dict may be empty, but then you must implement locators_dict property
            table_header_locator: css or xpath of a table header
            header_cell_locator: xpath of a singular cell in a header
            row_locator: css or xpath of a singular row
            row_type: the type of row in a table
        """
        super().__init__()

        self._container = root
        self._cell_locators = locators_dict
        self.body = self._container
        self.rows = self._container.all(row_locator)
        self.header = self._container.element(table_header_locator)
        self.header_cells = self.header.all(header_cell_locator)
        self.row_type: Type[R] = row_type

    @property
    def cell_locators(self):
        return self._cell_locators

    @report.step
    def get_row_by_cell_value(self, column_name, value) -> R:
        filtered_rows = self.rows.by_their(self.cell_locators[column_name], have.text(value))
        filtered_rows.should(have.size(1))
        return (
            self.row_type(filtered_rows.first, cell_locators=self.cell_locators)
            .as_(f'row_with_"{column_name}"="{value}"')
            .set_previous_name_chain_element(self)
        )

    @report.step
    def should_have_a_row_with(self, column_name, value):
        self.get_row_by_cell_value(column_name=column_name, value=value)

    def get_row_by_index(self, index) -> R:
        return (
            self.row_type(self.rows[index], cell_locators=self.cell_locators)
            .as_(f"row_number#{index + 1}")
            .set_previous_name_chain_element(self)
        )

    @report.step
    def is_row_presented(self, column_name, value) -> bool:
        result = self.rows.by_their(self.cell_locators[column_name], have.text(value))
        return bool(result)

    @property
    def last_remaining_row(self) -> R:
        self.rows.should(have.size(1))
        return (
            self.row_type(self.rows.first, cell_locators=self.cell_locators)
            .as_("last_remaining_row")
            .set_previous_name_chain_element(self)
        )

    @report.step
    def all_rows_should_have_value_in_column(self, column_name, value):
        self.rows.all(self.cell_locators[column_name]).should(have.exact_text(value).each)

    @report.step
    def all_rows_should_have_one_of_values_in_column(self, column_name, value_1, value_2):
        self.rows.all(self.cell_locators[column_name]).should(
            have.exact_text(value_1).or_(have.exact_text(value_2)).each
        )

    @report.step
    def should_be_loaded(self):
        """Right after loading a page table can give wrong results. For example, method get_row_smartly. To prevent it,
        use this method first"""
        self.rows.should(have.size_greater_than(0))
        self.rows.should(have.no.exact_text("").each)


class StandardCellsTable(Table[R]):
    def __init__(
        self,
        root: Element,
        column_names: Tuple[str, ...],
        table_header_locator: CSS_or_XPATH = "thead",
        header_cell_locator: XPATH = ".//th",
        row_locator: CSS_or_XPATH = ".//tbody//tr",
        body_cell_locator: XPATH = ".//td",
        row_type: Type[R] = TableRowWithMenu,
    ):
        """
        This table class may be used when all columns in your table have a regular structure
        (for example first_cell = //td[0],second_cell = //td[1], ...).
         With this class, it's possible to pass only column_names, and it will automatically define all cells in a row.
         It should work even if your table has movable columns.
         When a table has irregular cell locators (for example, in case of paired cells) you should use
         the original Table class and pass locators for every single cell.

        Args:
            root: the element where to look for the table
            column_names: names of columns
            table_header_locator: css or xpath of a table header relative to the table root
            header_cell_locator: xpath of a single header cell relative to the table header
            row_locator: css or xpath of a single row relative to the table
            body_cell_locator: xpath of a cell relative to the row
            row_type: the type of row in the table. Useful to customize rows with buttons or menus.
        """
        super().__init__(
            root=root,
            locators_dict=None,
            header_cell_locator=header_cell_locator,
            row_locator=row_locator,
            table_header_locator=table_header_locator,
            row_type=row_type,
        )
        self.column_names = column_names
        self._body_cell_locator = body_cell_locator
        self._header_cell_locator = header_cell_locator

    @cached_property
    def cell_locators(self) -> Dict[str, CSS_or_XPATH]:
        """
        This function defines cell locators by calculating the number of column with some name in a header.
        Pay attention that it can work only when page is loaded.
        If the order of the columns is changed, you need to clear the cache and recalculate the locators_dict.
        """
        self._container.should(be.present)
        locators_dict = {}
        for column_name in self.column_names:
            locators_dict[column_name] = f"{self._body_cell_locator}[{self._get_column_index_by_name(column_name)}]"
        return locators_dict

    def _get_column_index_by_name(self, column_name):
        return (
            len(
                self.header.element(f"{self._header_cell_locator}[.//text()='{column_name}']").all(
                    "./preceding-sibling::*"
                )
            )
            + 1
        )


class TableWithFilters(BaseElement, Generic[T, R]):
    def __init__(
        self,
        root: Element,
        tag_names: Tuple[str, ...],
        table: T,
        tags_locator=by.class_starts_with("FilterSearchWrapper_filterTags"),
        selected_tags_locator=by.class_contains("Tag-module_active"),
        filters_locator=by.class_starts_with("TableWithFilter_filtersWrapper"),
    ):
        super().__init__()
        self.tag_names = tag_names
        self._container = root
        self.filters: Element = self._container.element(filters_locator)
        self.tags: Collection = self.filters.element(tags_locator).all("button")
        self.selected_tag: Element = self.filters.element(selected_tags_locator)
        self.search_module: Element = self.filters.element(by.class_starts_with("SearchInput-module"))
        self.search_field: Element = self.search_module.element("input")
        self.search_field_reset_button: Element = self.search_module.element("button")
        self.results = table

    @report.step
    def search(self, text):
        self.search_field.clear()
        self.search_field.type(text)

    @report.step
    def get_row_smartly(self, column_name: str, value: str) -> R:
        """If row with the value is already not presented in search results, use search.
        Then returns related TableRow object

        Args:
            column_name: where to search value
            value:  what to search in a table

        Returns: related TableRow object
        """
        if not self.results.is_row_presented(column_name, value):
            self.search(value)
        return self.results.get_row_by_cell_value(column_name, value)

    @property
    def active_tag_text(self) -> str:
        result = self.selected_tag.get(query.text) if self.selected_tag.matching(be.present) else None
        return result

    @report.step
    def make_tag_selected(self, tag_text):
        if tag_text not in self.tag_names:
            raise KeyError(f'No such tag "{tag_text}". Possible tags are {self.tag_names}')
        if not self.active_tag_text or self.active_tag_text != tag_text:
            self.tags.element_by(have.exact_text(tag_text)).click()
        self.selected_tag.should(have.text(tag_text))

    @report.step
    def cancel_any_active_tag(self):
        if self.selected_tag.matching(be.present):
            self.selected_tag.click().should(be.absent)
