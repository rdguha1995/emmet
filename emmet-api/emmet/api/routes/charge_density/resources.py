from maggma.api.resource import ReadOnlyResource
from maggma.api.query_operator import PaginationQuery, SparseFieldsQuery
from emmet.core.charge_density import ChgcarDataDoc
from emmet.api.routes.charge_density.query_operators import ChgcarTaskIDQuery
from emmet.api.core.global_header import GlobalHeaderProcessor


def charge_density_resource(s3_store):
    resource = ReadOnlyResource(
        s3_store,
        ChgcarDataDoc,
        query_operators=[
            ChgcarTaskIDQuery(),
            PaginationQuery(default_limit=5, max_limit=10),
            SparseFieldsQuery(
                ChgcarDataDoc, default_fields=["task_id", "last_updated"],
            ),
        ],
        header_processor=GlobalHeaderProcessor(),
        tags=["Charge Density"],
        enable_default_search=True,
        enable_get_by_key=True,
        disable_validation=True,
    )

    return resource
