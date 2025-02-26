from maggma.api.query_operator import PaginationQuery, SparseFieldsQuery
from maggma.api.resource import ReadOnlyResource

from emmet.api.routes.materials.materials.query_operators import (
    ChemsysQuery,
    ElementsQuery,
    FormulaQuery,
)
from emmet.api.routes.materials.tasks.hint_scheme import TasksHintScheme
from emmet.api.routes.materials.tasks.query_operators import (
    DeprecationQuery,
    MultipleTaskIDsQuery,
    TrajectoryQuery,
    EntryQuery,
    LastUpdatedQuery,
)
from emmet.api.core.global_header import GlobalHeaderProcessor
from emmet.api.core.settings import MAPISettings
from emmet.core.tasks import DeprecationDoc, TaskDoc, TrajectoryDoc, EntryDoc

timeout = MAPISettings().TIMEOUT


def task_resource(task_store):
    resource = ReadOnlyResource(
        task_store,
        TaskDoc,
        query_operators=[
            FormulaQuery(),
            ChemsysQuery(),
            ElementsQuery(),
            MultipleTaskIDsQuery(),
            LastUpdatedQuery(),
            PaginationQuery(),
            SparseFieldsQuery(
                TaskDoc,
                default_fields=["task_id", "formula_pretty", "last_updated"],
            ),
        ],
        header_processor=GlobalHeaderProcessor(),
        hint_scheme=TasksHintScheme(),
        tags=["Materials Tasks"],
        sub_path="/tasks/",
        timeout=timeout,
        disable_validation=True,
    )

    return resource


def task_deprecation_resource(materials_store):
    resource = ReadOnlyResource(
        materials_store,
        DeprecationDoc,
        query_operators=[DeprecationQuery(), PaginationQuery()],
        tags=["Materials Tasks"],
        enable_get_by_key=False,
        enable_default_search=True,
        sub_path="/tasks/deprecation/",
        header_processor=GlobalHeaderProcessor(),
        timeout=timeout,
    )

    return resource


def trajectory_resource(task_store):
    resource = ReadOnlyResource(
        task_store,
        TrajectoryDoc,
        query_operators=[TrajectoryQuery(), PaginationQuery()],
        key_fields=["task_id", "calcs_reversed"],
        tags=["Materials Tasks"],
        sub_path="/tasks/trajectory/",
        header_processor=GlobalHeaderProcessor(),
        timeout=timeout,
        disable_validation=True,
    )

    return resource


def entries_resource(task_store):
    resource = ReadOnlyResource(
        task_store,
        EntryDoc,
        query_operators=[EntryQuery(), PaginationQuery()],
        key_fields=[
            "task_id",
            "input",
            "output",
            "run_type",
            "task_type",
            "completed_at",
            "last_updated",
        ],
        tags=["Materials Tasks"],
        sub_path="/tasks/entries/",
        header_processor=GlobalHeaderProcessor(),
        timeout=timeout,
        disable_validation=True,
    )

    return resource
