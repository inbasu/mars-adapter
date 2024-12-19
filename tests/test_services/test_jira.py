import pytest

from services.jira.connections.api_connection import JiraAPIClient
from services.jira.jira import Jira
from tests.fixtures import insight_mars_client as client  # noqa: F401


@pytest.mark.asyncio(loop_scope="session")
async def test_get_item(client: JiraAPIClient):
    obj = await Jira.get_issues(client, params={"jql":"key = IT-796953"})
    print(obj)    