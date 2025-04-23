# encoding: utf8
from typing import TYPE_CHECKING
from impala.dbapi import connect
from rocketx.providers.common.sql.hooks.sql import DbApiHook


if TYPE_CHECKING:
    from impala.interface import Connection


class ImpalaHook(DbApiHook):
    """Interact with Apache Impala through impyla."""
    conn_type = "impala"
    hook_name = "Impala"

    def get_conn(self) -> Connection:
        """
        Returns a connection to the Impala database.
        """
        return connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.schema,
            **self.extra
        )

