from . import Configuration, ApiClient
from .apis import AnalyzerApi, ParserApi, ResultsApi
from .models import (
    MapFileRequest,
    MapFileResponse,
    MapFileParseRequest,
    MapFileParseResponse,
    ClassificationRule,
)
import base64
from typing import Optional, List
import os
import urllib3
from datetime import datetime
from dataclasses import dataclass

urllib3.disable_warnings()
from opentelemetry.instrumentation.urllib3 import URLLib3Instrumentor

__all__ = ["ClientWrapper", "MapFileResponse", "SummaryResult"]


@dataclass
class SummaryResult:
    build_number: str
    build_sequence: int
    branch: str
    build_name: str
    board: str
    compiler: str
    application_name: str
    stack: str
    target: str
    row_create_date_time: str
    summary_json: dict
    summary_ext_json: Optional[dict]
    sdk_commit_hash: Optional[str]


class ClientWrapper:
    def __init__(self, server_url=None, verify_ssl=True):
        URLLib3Instrumentor().instrument()
        config = Configuration(host=server_url)
        config.proxy = os.environ.get("https_proxy")
        if not verify_ssl:
            config.verify_ssl = False

        self.client = ApiClient(config)
        self._analyzer_api = AnalyzerApi(self.client)
        self._parser_api = ParserApi(self.client)
        self._results_api = ResultsApi(self.client)

    def get_app_summary_records(
        self,
        stack_name: str,
        app_name: str,
        branches: list[str],
        sdk_commit_hashes: list[str],
        target_part: Optional[str] = None,
        target_board: Optional[str] = None,
        compiler: Optional[str] = None,
        build_number: Optional[str] = None,
    ) -> List[SummaryResult]:
        results = self._results_api.get_app_summary_records(
            stack_name,
            app_name,
            branch=list(branches),
            sdk_commit_hash=list(sdk_commit_hashes),
        )
        # group results by build_name, compiler, target_part, target_board
        grouped_results = {}
        for r in results:
            result = SummaryResult(**r)
            if compiler and result.compiler != compiler:
                continue
            if target_part and result.target != target_part:
                continue
            if target_board and result.board != target_board:
                continue
            if build_number and result.build_number != build_number:
                continue
            key = (
                result.build_name,
                result.compiler,
                result.target,
                result.board,
            )
            create_date_time = datetime.fromisoformat(result.row_create_date_time)
            if key in grouped_results:
                existing_create_date_time = datetime.fromisoformat(
                    grouped_results[key].row_create_date_time
                )
                if create_date_time > existing_create_date_time:
                    grouped_results[key] = result
            else:
                grouped_results[key] = result

        all_results = [item for _, item in grouped_results.items()]
        return all_results

    def parse_map_file(self, map_file_path: str):
        with open(map_file_path, "rb") as f:
            base64_encoded_map_file = base64.b64encode(f.read()).decode("utf-8")
        parse_request = MapFileParseRequest(base64_encoded_map_file)
        return self._parser_api.parse_map_file(parse_request)

    def analyze_map_file(
        self,
        map_file_path: str,
        stack_name: str,
        target_part: str,
        compiler: str,
        project_file_path: Optional[str] = None,
        classification_rules: Optional[List[ClassificationRule]] = None,
        ignore_default_rules: Optional[bool] = False,
        target_board: Optional[str] = None,
        app_name: Optional[str] = None,
        branch_name: Optional[str] = None,
        build_number: Optional[str] = None,
        sdk_commit_hash: Optional[str] = None,
        store_results: bool = False,
        uc_component_branch_name: Optional[str] = None,
        code_size_upper_threshold: Optional[int] = None,
        code_size_lower_threshold: Optional[int] = None,
        ram_size_upper_threshold: Optional[int] = None,
        ram_size_lower_threshold: Optional[int] = None,
        alert_notification_topic_id: Optional[str] = None,
        **_kwargs
    ) -> MapFileResponse:
        with open(map_file_path, "rb") as f:
            base64_encoded_map_file = base64.b64encode(f.read()).decode("utf-8")
        base64_encoded_project_file = None
        if project_file_path is not None:
            with open(project_file_path, "rb") as f:
                base64_encoded_project_file = base64.b64encode(f.read()).decode("utf-8")
        if classification_rules is None:
            classification_rules = []
        kwargs = dict(
            target_board=target_board,
            app_name=app_name,
            branch_name=branch_name,
            build_number=build_number,
            commit=sdk_commit_hash,
            store_results=store_results,
            uc_component_branch_name=uc_component_branch_name,
            code_size_upper_threshold=code_size_upper_threshold,
            code_size_lower_threshold=code_size_lower_threshold,
            ram_size_upper_threshold=ram_size_upper_threshold,
            ram_size_lower_threshold=ram_size_lower_threshold,
            alert_notification_topic_id=alert_notification_topic_id,
        )
        for key in list(kwargs.keys()):
            if kwargs[key] is None:
                kwargs.pop(key)

        map_file_request = MapFileRequest(
            map_file=base64_encoded_map_file,
            stack_name=stack_name,
            target_part=target_part,
            compiler=compiler,
            classification_rules=classification_rules,
            ignore_default_rules=ignore_default_rules,
            **kwargs
        )
        if base64_encoded_project_file is not None:
            map_file_request.project_file = base64_encoded_project_file
            map_file_request.project_file_name = os.path.basename(project_file_path)
        return self._analyzer_api.analyze_map_file(map_file_request)
