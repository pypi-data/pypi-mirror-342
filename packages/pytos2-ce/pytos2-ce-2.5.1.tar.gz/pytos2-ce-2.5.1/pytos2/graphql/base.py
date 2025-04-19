from typing import Optional, Tuple
from .models import GraphResponse, Variables

from ..api import GraphqlError, OAuth2APISession


class BaseGql:
    hostname: Optional[str]
    username: Optional[str]
    password: Optional[str]
    session: Optional[OAuth2APISession]

    def raw_query(self, query: str, variables: Variables = None) -> GraphResponse:
        """
        Execute a GraphQL query and return the raw GraphQL response as a python dictionary.

        Usage:
            # Example 1:
            data = st.graphql.raw_query("query rules($first: Int) { rules { values(first: $first, offset: 0) { id } } }", variables={"first": 100})

        """
        json = (
            {"query": query, "variables": variables} if variables else {"query": query}
        )

        response = self.session.post("graphql", json=json)
        response.raise_for_status()

        res = response.json()
        if "errors" in res:
            raise GraphqlError(errors=res["errors"])

        return response.json()
