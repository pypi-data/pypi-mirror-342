import asyncio
from typing import Any, Dict, List, Tuple
from urllib.parse import urlencode

import click
from gql.transport.requests import RequestsHTTPTransport
import gql
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

import requests

from upwork_fetcher.config import load_config, save_config
from upwork_fetcher.models.dbcontext import dbcontext
from upwork_fetcher.models.jobs import Job
from upwork_fetcher.queries.market_place_job import MarketplaceJobPostingsSearchQuery
from upwork_fetcher.schema import JobSchema

console = Console()


# CLIENT_ID = "13417fab9471a23c91ba14de24089ec3"  # Replace with your Upwork client ID
# CLIENT_SECRET = "db7c0b78592ad05b"  # Replace with your Upwork client secret
# REDIRECT_URI = "http://localhost:8000/upwork-callback"  # Replace with your redirect URI
# CODE = "ab09c682a28f7423b4e3f3018bb9b045"
# Upwork API URLs
AUTH_URL = "https://www.upwork.com/ab/account-security/oauth2/authorize"
TOKEN_URL = "https://www.upwork.com/api/v3/oauth2/token"


class UpworkService:

    def __init__(self, client_id: str, client_secret: str, redirect_uri: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri

    def fetch(
        self,
        search_expressions: Tuple[str] | None,
        skill_expressions: Tuple[str] | None,
        title_expressions: Tuple[str] | None,
        db_url: str,
        offset: int = 0,
        limit: int = 50,
    ):
        with console.status("Refreshing Access Token..."):
            self.refresh_access_token()

        search_expression = ", ".join(search_expressions or [])
        skill_expression = ", ".join(skill_expressions or [])
        title_expression = ", ".join(title_expressions or [])

        console.print(
            Panel.fit(
                f"""
                Starting to fetch jobs about : 
                Search Expressions: '{search_expression}'
                Skill Expressions: '{skill_expression}'
                Title Expressions: '{title_expression}'
                """,
                title="[bold]Text Processing CLI[/bold]",
                title_align="left",
            )
        )

        with console.status(f"searching on jobs..."):
            data = self.fetch_data(
                search_expression, skill_expression, title_expression, offset, limit
            )

        if data is None:
            console.print(
                f"""
                [bold red]Failed to fetch jobs about: 
                Search Expressions: '{search_expression}'
                Skill Expressions: '{skill_expression}'
                Title Expressions: '{title_expression}'
                """
            )
            raise click.Abort()

        console.print(f"[bold green]{len(data)} jobs fetched successfully.")

        jobs = self.convert_dict_to_job_schema(data)

        self._draw_table(jobs, table_title=f"Jobs")

        with console.status(f"Saving jobs into DB...") as status:
            data, new_data = asyncio.get_event_loop().run_until_complete(
                self.split_data(jobs)
            )
            status.console.print(f"{len(new_data)} new jobs found")

            new_data = asyncio.get_event_loop().run_until_complete(
                self.save_to_db(new_data)
            )
            status.console.print(f"{len(new_data)} jobs saved to DB")

    def _draw_table(self, jobs: List[JobSchema], table_title: str = "Fetched jobs"):
        table = Table(title=table_title, show_header=True, header_style="bold magenta")
        table.add_column("#", style="dim", justify="left")
        table.add_column("ID", style="dim", justify="left")
        table.add_column("Job Title", justify="left")

        for index, job in enumerate(jobs, start=1):
            table.add_row(str(index), job.id, job.title)

        console.print(table)

    async def split_data(self, data: List[JobSchema]):
        config = load_config()
        async with dbcontext.db_context(db_url=config.get("db_url")):
            ids: List[str] = [job.id for job in data]
            existing_records: List[Dict[str, Any]] = await Job.filter(
                id__in=ids
            ).values("id")
            existing_ids: set[str] = {record["id"] for record in existing_records}

            # Filter out existing data
            new_data: List[JobSchema] = [
                job for job in data if job.id not in existing_ids
            ]

            # console.print(f"{len(new_data)} new jobs found")
            return data, new_data

    async def save_to_db(self, data: List[JobSchema]):
        config = load_config()
        async with dbcontext.db_context(db_url=config.get("db_url")):

            list_of_jobs: List[Job] = []
            for job in data:
                list_of_jobs.append(Job(**job.model_dump()))

            await Job.bulk_create(list_of_jobs, ignore_conflicts=True)

        return data

    def get_authorization_url(self):
        """Returns the authorization URL for the Upwork API to get the code."""
        params = {
            "client_id": self.client_id,
            "response_type": "code",
            "redirect_uri": self.redirect_uri,
        }
        return f"{AUTH_URL}?{urlencode(params)}"

    def get_access_token(self, code: str):
        data = {
            "grant_type": "authorization_code",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
            "redirect_uri": self.redirect_uri,
        }
        response = requests.post(
            TOKEN_URL,
            data=data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

        response.raise_for_status()
        return response.json()

    # def get_refresh_token(self, auth_code: str):
    def _get_refresh_token_and_refresh_token(self, refresh_token: str):
        data = {
            "grant_type": "refresh_token",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": refresh_token,
        }
        response = requests.post(TOKEN_URL, data=data)
        response.raise_for_status()
        return response.json()

    def refresh_access_token(self):
        config = load_config()

        refresh_token = config["refresh_token"]

        new_tokens = self._get_refresh_token_and_refresh_token(refresh_token)

        self.access_token = new_tokens["access_token"]

        save_config(
            {
                "access_token": new_tokens["access_token"],
                "refresh_token": new_tokens["refresh_token"],
                "expires_in": new_tokens["expires_in"],
            }
        )
        # click.echo(load_config())

    def fetch_data(
        self,
        search_expression: str | None,
        skill_expression: str | None,
        title_expression: str | None,
        offset: int = 0,
        limit: int = 50,
    ):

        # Define the transport with headers for authentication or other purposes
        transport = RequestsHTTPTransport(
            url="https://api.upwork.com/graphql",
            headers={
                "Authorization": f"Bearer {self.access_token}",
            },
        )

        # Create a GraphQL client
        client = gql.Client(transport=transport, fetch_schema_from_transport=True)

        # Define a query
        query = gql.gql(MarketplaceJobPostingsSearchQuery)
        # for search_expression in search_expressions:
        variable_values: Dict[str, Any] = {
            "marketPlaceJobFilter": {
                "searchExpression_eq": search_expression,
                "pagination_eq": {"after": str(offset), "first": limit},
            },
            "searchType": "JOBS_FEED",
            # "jobType_eq": "HOURLY", # FIXED
            "sortAttributes": [{"field": "RECENCY"}],
        }
        if search_expression:
            variable_values["marketPlaceJobFilter"][
                "searchExpression_eq"
            ] = search_expression
        if skill_expression:
            variable_values["marketPlaceJobFilter"][
                "skillExpression_eq"
            ] = skill_expression
        if title_expression:
            variable_values["marketPlaceJobFilter"][
                "titleExpression_eq"
            ] = title_expression

        try:
            result = client.execute(  # type: ignore
                document=query,
                variable_values=variable_values,
            )
            return result["marketplaceJobPostingsSearch"]["edges"]

        except Exception as e:
            click.echo(str(e))

    def convert_dict_to_job_schema(self, data: List[Dict[str, Any]]) -> List[JobSchema]:
        return [JobSchema.create_instance(edge["node"]) for edge in data]
