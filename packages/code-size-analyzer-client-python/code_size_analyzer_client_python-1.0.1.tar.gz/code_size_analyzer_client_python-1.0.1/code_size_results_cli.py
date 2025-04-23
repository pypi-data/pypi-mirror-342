import click
from code_size_analyzer_client.client_wrapper import ClientWrapper
import json
from otel_extensions import (
    init_telemetry_provider,
    TelemetryOptions,
    flush_telemetry_data,
)
import logging
from dataclasses import asdict

query_summary_help = "Query code size application summary records"


@click.group()
def cli():
    pass


@cli.command(help=query_summary_help, short_help=query_summary_help)
@click.option(
    "--stack-name",
    "--stack_name",
    required=True,
    help="stack owner name (i.e. zigbee, matter)",
)
@click.option("--app-name", "--app_name", required=True, help="application name")
@click.option(
    "--target-part",
    "--target_part",
    default=None,
    help="target part (e.g. efr32mg22c224f512im40)",
)
@click.option("--compiler", default=None, help="compiler name (gcc or iar)")
@click.option(
    "--target-board",
    "--target_board",
    default=None,
    help="target board (e.g. brd4181a)",
)
@click.option(
    "--build-number",
    "--build_number",
    default=None,
    type=str,
    help="build number (e.g. b1544 or 1544)",
)
@click.option(
    "--branch-name",
    "--branch_name",
    "--branch",
    default=None,
    multiple=True,
    help="branch name",
)
@click.option(
    "--sdk-commit-hash",
    "--sdk_commit_hash",
    "--commit",
    default=None,
    multiple=True,
    help="SDK commit hash",
)
@click.option("--output-file", "-o", default=None, help="output file")
@click.option(
    "--service-url",
    "--service_url",
    default="https://code-size-analyzer.silabs.net",
    help="service endpoint",
)
@click.option(
    "--verify-ssl",
    "--verify_ssl",
    default=False,
    help="verify ssl certificate on server",
)
def query_summary(
    stack_name,
    target_part,
    compiler,
    service_url,
    verify_ssl,
    target_board,
    app_name,
    branch_name,
    build_number,
    sdk_commit_hash,
    output_file,
):
    logging.getLogger("opentelemetry.util._time").setLevel(logging.ERROR)
    init_telemetry_provider(
        TelemetryOptions(
            OTEL_SERVICE_NAME="Code Size Analyzer CLI",
        )
    )
    client_wrapper = ClientWrapper(server_url=service_url, verify_ssl=verify_ssl)
    if build_number is not None and build_number.isdigit():
        build_number = f"b{build_number}"
    results = client_wrapper.get_app_summary_records(
        stack_name,
        app_name,
        branch_name,
        sdk_commit_hash,
        target_part,
        target_board,
        compiler,
        build_number,
    )
    output = json.dumps([asdict(r) for r in results], indent=2)
    if output_file:
        with open(output_file, "w") as f:
            f.write(json.dumps([asdict(r) for r in results], indent=2))
    else:
        print(output)

    flush_telemetry_data()


if __name__ == "__main__":
    cli()
