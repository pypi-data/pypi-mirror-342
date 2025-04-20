import os
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import AsyncIterator

from mcp.server.fastmcp import Context, FastMCP

from mcp_jenkins.jenkins import JenkinsClient


@dataclass
class JenkinsContext:
    client: JenkinsClient


@asynccontextmanager
async def jenkins_lifespan(server: FastMCP) -> AsyncIterator[JenkinsContext]:
    try:
        jenkins_url = os.getenv('jenkins_url')
        jenkins_username = os.getenv('jenkins_username')
        jenkins_password = os.getenv('jenkins_password')
        jenkins_timeout = int(os.getenv('jenkins_timeout'))

        client = JenkinsClient(
            url=jenkins_url,
            username=jenkins_username, password=jenkins_password,
            timeout=jenkins_timeout
        )

        # Provide context to the application
        yield JenkinsContext(client=client)
    finally:
        # Cleanup resources if needed
        pass


def client(ctx: Context) -> JenkinsClient:
    return ctx.request_context.lifespan_context.client


mcp = FastMCP('mcp-jenkins', lifespan=jenkins_lifespan)


# Import the job and build modules here to avoid circular imports
from mcp_jenkins.server import build, job  # noqa: E402, F401
