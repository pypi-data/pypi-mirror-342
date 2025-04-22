import json
import os

# ruff: noqa: I001
from aws_cdk import (
    Fn,
    Duration,
    aws_apigateway as apigw,
    aws_events as events,
    aws_events_targets as targets,
    aws_iam as iam,
    aws_lambda as _lambda,
    aws_lambda_event_sources as lambda_event_source,
    aws_sqs as sqs,
    aws_s3_assets as s3_assets,
)
from aws_cdk.aws_lambda import CfnFunction
from constructs import Construct

from wellapi.applications import Lambda, WellApi
from wellapi.build.packager import package
from wellapi.openapi.utils import get_openapi
from wellapi.utils import import_app, load_handlers

OPENAPI_FILE = "openapi-spec.json"
APP_LAYOUT_FILE = "app_content.zip"
DEP_LAYOUT_FILE = "layer_content.zip"


class WellApiCDK(Construct):
    """
    This class is used to create a Well API using AWS CDK.
    """

    def __init__(
        self,
        scope: Construct,
        id_: str,
        *,
        app_srt: str,
        handlers_dir: str,
    ) -> None:
        super().__init__(scope, id_)

        self.app_srt = app_srt
        self.handlers_dir = os.path.abspath(handlers_dir)

        wellapi_app: WellApi = self._package_app()

        # defining a Cfn Asset from the openAPI file
        open_api_asset = s3_assets.Asset(self, "OpenApiAsset", path=OPENAPI_FILE)
        transform_map = {"Location": open_api_asset.s3_object_url}
        data = Fn.transform("AWS::Include", transform_map)

        self.api = apigw.SpecRestApi(
            self,
            f"{wellapi_app.title}Api",
            api_definition=apigw.ApiDefinition.from_inline(data),
        )

        for q in wellapi_app.queues:
            queue = sqs.Queue(self, f"{q.queue_name}Queue", queue_name=q.queue_name)

        shared_layer = [
            _lambda.LayerVersion(
                self,
                "SharedLayer",
                code=_lambda.Code.from_asset(DEP_LAYOUT_FILE),
                compatible_runtimes=[_lambda.Runtime.PYTHON_3_12],  # type: ignore
                layer_version_name="shared_layer",
            )
        ]
        code_layer = _lambda.Code.from_asset(APP_LAYOUT_FILE)

        lmbd: Lambda
        for lmbd in wellapi_app.lambdas:
            lambda_function = _lambda.Function(
                self,
                f"{lmbd.arn}Function",
                function_name=f"{lmbd.arn}Function",
                runtime=_lambda.Runtime.PYTHON_3_12,  # type: ignore
                handler=lmbd.unique_id,
                memory_size=lmbd.memory_size,
                timeout=Duration.seconds(lmbd.timeout),
                code=code_layer,
                layers=shared_layer,  # type: ignore
            )

            if lmbd.type_ == "endpoint":
                lambda_function.add_permission(
                    f"{lmbd.arn}Permission",
                    principal=iam.ServicePrincipal("apigateway.amazonaws.com"),
                    action="lambda:InvokeFunction",
                    source_arn=self.api.arn_for_execute_api(lmbd.method.upper()),
                )

                cfn_lambda: CfnFunction = lambda_function.node.default_child  # type: ignore
                cfn_lambda.override_logical_id(f"{lmbd.arn}Function")
                # self.api.node.add_dependency(lambda_function)

            if lmbd.type_ == "queue":
                queue = sqs.Queue(
                    self,
                    f"{lmbd.name}Queue",
                    queue_name=lmbd.path,
                    visibility_timeout=Duration.seconds(lmbd.timeout),
                )

                sqs_event_source = lambda_event_source.SqsEventSource(queue)  # type: ignore

                # Add SQS event source to the Lambda function
                lambda_function.add_event_source(sqs_event_source)

            if lmbd.type_ == "job":
                rule = events.Rule(
                    self,
                    f"{lmbd.name}Rule",
                    schedule=events.Schedule.expression(lmbd.path),
                )

                rule.add_target(targets.LambdaFunction(lambda_function))  # type: ignore

    def _package_app(self) -> WellApi:
        wellapi_app = import_app(self.app_srt)
        load_handlers(self.handlers_dir)

        resp = get_openapi(
            title=wellapi_app.title,
            version=wellapi_app.version,
            openapi_version="3.0.1",
            description=wellapi_app.description,
            lambdas=wellapi_app.lambdas,
            tags=wellapi_app.openapi_tags,
            servers=wellapi_app.servers,
        )
        with open(OPENAPI_FILE, "w") as f:
            json.dump(resp, f)

        package(DEP_LAYOUT_FILE, APP_LAYOUT_FILE)

        return wellapi_app
