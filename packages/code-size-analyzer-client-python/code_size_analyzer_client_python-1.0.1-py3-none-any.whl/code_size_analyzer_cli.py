from __future__ import annotations

import json
import logging

import click
import yaml
from code_size_analyzer_client.api_client import ApiClient
from code_size_analyzer_client.client_wrapper import ClientWrapper
from otel_extensions import (
    TelemetryOptions,
    flush_telemetry_data,
    init_telemetry_provider,
)
from retry import retry


@click.command()
@click.option("--map_file", "--map-file", required=True, help="path to map file")
@click.option(
    "--stack_name",
    "--stack-name",
    required=True,
    help="stack owner name (i.e. zigbee, matter)",
)
@click.option(
    "--target_part",
    "--target-part",
    required=True,
    help="target part (e.g. efr32mg22c224f512im40)",
)
@click.option("--compiler", required=True, help="compiler name (gcc or iar)")
@click.option(
    "--project_file", "--project-file", default=None, help="path to project file"
)
@click.option(
    "--classification_rules_file",
    "--classification-rules-file",
    default=None,
    help="path to classification rules file",
)
@click.option(
    "--ignore_default_rules",
    "--ignore-default-rules",
    is_flag=True,
    help="If providing classification rules file, ignore the default rules and exclusively use the provided rules.",
)
@click.option(
    "--service_url",
    "--service-url",
    default="https://code-size-analyzer.silabs.net",
    help="service endpoint",
)
@click.option(
    "--output_file",
    "--output-file",
    default=None,
    help="path to output json file (default is to stdout)",
)
@click.option(
    "--verify_ssl",
    "--verify-ssl",
    default=False,
    help="verify ssl certificate on server",
)
@click.option(
    "--target_board",
    "--target-board",
    default=None,
    help="target board (e.g. brd4181a)",
)
@click.option("--app_name", "--app-name", default=None, help="application name")
@click.option("--branch_name", "--branch-name", default=None, help="branch name")
@click.option("--build_number", "--build-number", default=None, help="build number")
@click.option(
    "--sdk_commit_hash", "--sdk-commit-hash", default=None, help="SDK commit hash"
)
@click.option(
    "--store_results",
    "--store-results",
    default=False,
    help="store results to database",
)
@click.option(
    "--uc_component_branch_name",
    "--uc-component-branch-name",
    default=None,
    help="branch name for uc component-based categorization (e.g. use develop/22q4 for a feature branch branched off develop/22q4)",
)
@click.option(
    "--code-size-upper-threshold",
    default=None,
    type=int,
    help="code size upper threshold in bytes",
)
@click.option(
    "--code-size-lower-threshold",
    default=None,
    type=int,
    help="code size lower threshold in bytes",
)
@click.option(
    "--ram-size-upper-threshold",
    default=None,
    type=int,
    help="ram size upper threshold in bytes",
)
@click.option(
    "--ram-size-lower-threshold",
    default=None,
    type=int,
    help="ram size lower threshold in bytes",
)
@click.option(
    "--alert-notification-topic-id",
    default=None,
    type=str,
    help="ID of iot-notifications topic to send alerts to if thresholds are exceeded",
)
def main(
    map_file: str,
    stack_name: str,
    target_part: str,
    compiler: str,
    project_file: str | None,
    classification_rules_file: str | None,
    ignore_default_rules: bool,
    service_url: str | None,
    output_file: str | None,
    verify_ssl: bool,
    target_board: str | None,
    app_name: str | None,
    branch_name: str | None,
    build_number: str | None,
    sdk_commit_hash: str | None,
    store_results: bool,
    uc_component_branch_name: str | None,
    code_size_upper_threshold: int | None,
    code_size_lower_threshold: int | None,
    ram_size_upper_threshold: int | None,
    ram_size_lower_threshold: int | None,
    alert_notification_topic_id: str | None,
):
    logging.getLogger("opentelemetry.util._time").setLevel(logging.ERROR)
    init_telemetry_provider(
        TelemetryOptions(
            OTEL_SERVICE_NAME="Code Size Analyzer CLI",
        )
    )
    client_wrapper = ClientWrapper(server_url=service_url, verify_ssl=verify_ssl)

    if ignore_default_rules and not classification_rules_file:
        raise ValueError(
            "If ignore_default_rules is set, classification_rules_file must be provided."
        )

    classification_rules = None
    if classification_rules_file:
        with open(classification_rules_file) as f:
            classification_rules = yaml.safe_load(f)

    @retry(tries=6, delay=1, max_delay=10, backoff=2)
    def call_analyzer():
        r = client_wrapper.analyze_map_file(
            map_file,
            stack_name,
            target_part,
            compiler,
            project_file,
            classification_rules=classification_rules,
            ignore_default_rules=ignore_default_rules,
            target_board=target_board,
            app_name=app_name,
            branch_name=branch_name,
            build_number=build_number,
            sdk_commit_hash=sdk_commit_hash,
            store_results=store_results,
            uc_component_branch_name=uc_component_branch_name,
            code_size_upper_threshold=code_size_upper_threshold,
            code_size_lower_threshold=code_size_lower_threshold,
            ram_size_upper_threshold=ram_size_upper_threshold,
            ram_size_lower_threshold=ram_size_lower_threshold,
            alert_notification_topic_id=alert_notification_topic_id,
        )
        j = json.dumps(ApiClient.sanitize_for_serialization(r), indent=2)
        if output_file is not None:
            with open(output_file, "w") as f:
                f.write(j)
        else:
            print(j)

    call_analyzer()
    flush_telemetry_data()


if __name__ == "__main__":
    main()
