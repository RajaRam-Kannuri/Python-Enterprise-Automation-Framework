from typing import Any, Generic, TypeVar

from core.models.lms.lms_base import LMSGenericModelBase, LMSModelBase

T = TypeVar("T")


class LoadOptions(LMSModelBase):
    """
    LoadOptions = {
       // implementation queue 1
        skip?: number;
        take?: number;

        sort?: SortDescriptor | SortDescriptor[];

        filter?: FilterDescriptor | FilterDescriptor[];
        requireTotalCount?: boolean;

      // implementation queue 2
        totalSummary?: SummaryDescriptor<T> | Array<SummaryDescriptor<T>>;

      // implementation queue 3
        group?: GroupDescriptor | GroupDescriptor[];
        groupSummary?: SummaryDescriptor | SummaryDescriptor[];
        requireGroupCount?: boolean;
    }

    SortDescriptor=GroupDescriptor=
    {
        selector: string;
        desc?: boolean;   //default=false
    }

    SummaryDescriptor = {
        selector: string;
        summaryType?: 'sum' | 'avg' | 'min' | 'max' | 'count';   // default = count
    }

    FilterDescriptor = [column, op, value]
    | [FilterDescriptor, binop, FilterDescriptor]
    | ["!", FilterDescriptor]

    op = "=" | "<>" | ">" | ">=" | "<" | "<=" | "startswith" | "endswith" | "contains" | "notcontains"
    binop = "and" | "or"
    """

    skip: int | None = None
    take: int | None = None
    sort: str | None = None
    filter: str | None = None
    requireTotalCount: bool | None = None


class QueryResponse(LMSGenericModelBase, Generic[T]):
    data: list[T]
    total_count: int | None = None
    summary: list[Any] | None = None
    group_count: int | None = -1
