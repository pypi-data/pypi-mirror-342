"""Main entry point for MCP Description Server."""

from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("Description about projects and instructions about tasks")

__version__ = "0.1.17"


@mcp.tool()
async def just_get_version():
    """
    Get the version of the MCP protocol being used. currently:0.1.176

    Returns:
        str: The version of the MCP protocol.
    """
    return __version__


@mcp.tool()
async def get_instructions() -> str:
    """
    Get instructions for the project.
    """
    return """I'm working on a spring cloud project. Here are some basic information about my project:
0. As a Chinese team, we typically use Chinese for communication, while I use English to talk to LLMs and AI-IDEs like cursor and Github Copilot.
1. We use ZuulGateway for routing and load balancing, eureka for service discovery, and apache nacos for configuration management.
2. Most services use MySQL for data storage, and we use Redis for caching.
3. Some projects use RabbtMQ for message queue.
4. We have the following environments: dev-integ (开发联调环境), test (测试环境), test-integ (集成环境), prod (生产环境). The spring boot profiles are named like those, but with different names as developers use different names and we haven't enforce a naming convention yet.
5. The resources folder in Java projects are crucial, as they contain info about different environments and the info about the middlewares like MySQL, redis. Some projects, however, use Nacos for configuration management, so sometimes you need to check out nacos for the configuration.
6. For the nacos-configrated projects, the `bootstrap.yml` is crucial, so you should check it out first. You can use nacos tool to get the configuration info. Some of these projects use mixed-configuration, it has both nacos and local configuration. In this case, you may need to checkout both the `bootstrap.yml` then traverse to the nacos server and the `application.yml` files, and then combine the configuration info.
7. The server tool is very useful for remote service debugging, as some of our deployed services may have trouble and you may need to ssh into the server I provided to you and see logs and/or service stats like CPU, network, memory, etc.
"""


def main():
    """Run the MCP Description server when called directly."""
    print(f"Starting MCP Description Server for version {__version__}...")
    mcp.run()  # The FastMCP API doesn't accept host and port parameters


if __name__ == "__main__":
    main()
