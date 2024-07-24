import datetime
import logging
from typing import Optional

from metadata.generated.schema.entity.data.table import Table
from metadata.generated.schema.entity.data.dashboard import Dashboard
from metadata.generated.schema.entity.data.pipeline import Pipeline
from metadata.workflow.application import AppRunner
from metadata.ingestion.ometa.models import EntityList

from metadata.community.applications.OpenMetadataRetention.generated.config import (
    OpenMetadataRetentionConfig,
)

logger = logging.getLogger("openmetadata_retention")


class Pager:
    """Pager class to paginate through the results"""

    def __init__(self, next_page_func):
        self.next_page_func = next_page_func
        self.page: EntityList = None
        self.page_num = -1

    def done(self):
        return self.page is not None and self.page.after is None

    def __iter__(self):
        while not self.done():
            after = self.page.after if self.page is not None else None
            self.page = self.next_page_func(after=after)
            self.page_num += 1
            print(f"Page {self.page_num}")
            yield from self.page.entities


class OpenMetadataRetention(AppRunner):
    """
    OpenMetadataRetention Application
    You can execute it with `python -m metadata app -c examples/config.yaml`
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        config = self.app_config.model_dump()
        del config["type"]
        self.app_config = OpenMetadataRetentionConfig.model_validate(config)

    @property
    def name(self) -> str:
        return "MetadataRetention"

    def run(self) -> None:
        print(self.app_config)
        now = datetime.datetime.now()
        retention_period = datetime.timedelta(seconds=self.app_config.retentionSeconds)
        print(f"Running on {now} and deleting tables older than {retention_period}")
        expire_after = (now.timestamp() - retention_period.total_seconds()) * 1000
        version = self.metadata.get_server_version()
        print(f"Running retention on tables with server version {version}")
        for entity_type in [
            Table,
            Dashboard,
            Pipeline,
        ]:
            print(f"Running retention on {entity_type.__name__}")

            def next_page(after: Optional[str]):
                return self.metadata.list_entities(entity_type, after=after)

            pager = Pager(next_page)
            for entity in pager:
                self.expire(entity, expire_after)

    def close(self) -> None:
        pass

    def expire(self, entity: Table, expire_after: int) -> None:
        if entity.updatedAt.root < expire_after:
            print(f"Deleting {type(entity).__name__}: {entity.fullyQualifiedName.root}")
            self.metadata.delete(type(entity), entity.id)
        else:
            print(f"Entity {entity.fullyQualifiedName.root} is not due for deletion")
