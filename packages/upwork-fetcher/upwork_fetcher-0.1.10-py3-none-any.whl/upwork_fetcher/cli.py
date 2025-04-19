import click

from upwork_fetcher.config import load_config
from upwork_fetcher.commands import fetch, setup


@click.group()
@click.version_option()
@click.pass_context
def cli(ctx: click.Context):
    config = load_config()
    ctx.obj = config


cli.add_command(fetch)
cli.add_command(setup)


# async def async_main():
#     await cli.main(standalone_mode=False)


# if __name__ == "__main__":
#     import asyncio

#     asyncio.run(async_main())
