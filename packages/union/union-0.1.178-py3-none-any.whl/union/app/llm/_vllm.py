import shlex
from dataclasses import dataclass
from typing import List, Union

from union.app import App, Input

_VLLM_MODEL_NAME = "vllm-model"


@dataclass
class VLLMApp(App):
    """
    App backed by FastAPI.

    :param name: The name of the application.
    :param container_image: The container image to use for the application.
    :param args: Entrypoint to start application.
    :param command: Command to start application.
    :param port: Port application listens to. Currently, this must be 8080 and the application
        must listen on 8080.
    :param requests: Compute resource requests for application.
    :param secrets: Secrets that are requested for application.
    :param limits: Compute resource limits for application.
    :param include: Files to include for your application.
    :param inputs: Inputs for the application.
    :param env: Environment variables to set for the application.
    :param min_replicas: Minimum number of replicas (ignore if autoscaling is set).
    :param max_replicas: Maximum number of replicas (ignore if autoscaling is set).
    :param scaledown_after: Time to wait before scaling down a replica after it has been idle.
    :param scaling_metric: Autoscale based on a parameter, e.g. request rate or concurrency
      (others may be added in the future).
    :param cluster_pool: The target cluster_pool where the app should be deployed.
    :param requires_auth: Public URL does not require any authentication
    :param type: Type of app
    :param description: Description of app
    :param subdomain: Custom subdomain for your app.
    :param extra_args: Extra args to pass to `vllm serve`. See
        https://docs.vllm.ai/en/stable/serving/engine_args.html for details.
    :param model: Artifact URI for model. It should start with `flyte://`
    :param model_id: model id that is exposed by vllm.
    :param stream_model: Set to True to stream model from blob store to the GPU directly.
      If False, the model will be downloaded to the local file system first and then loaded
      into the GPU.
    """

    port: int = 8000
    type: str = "vLLM"
    extra_args: Union[str, List[str]] = ""
    # In the future support ArtifactQuery
    model: str = ""
    model_id: str = ""
    stream_model: bool = True

    def __post_init__(self):
        if self.model == "":
            raise ValueError("model must be defined")

        if self.model_id == "":
            raise ValueError("model_id must be defined")

        if self.args:
            raise ValueError("args can not be set for VLLMApp. Use `extra_args` to add extra arguments to vllm")

        if isinstance(self.extra_args, str):
            extra_args = shlex.split(self.extra_args)
        else:
            extra_args = self.extra_args

        self.args = [
            "union-model-loader-vllm",
            "serve",
            "/root/union",
            "--served-model-name",
            self.model_id,
            "--port",
            str(self.port),
            *extra_args,
        ]

        if self.inputs:
            raise ValueError("inputs can not be set for VLLMApp")

        self.inputs = [
            Input(
                name=_VLLM_MODEL_NAME,
                value=self.model,
                type=Input.Type._ArtifactUri,
                env_var="UNION_MODEL_LOADER_REMOTE_MODEL_PATH",
                download=False,
            )
        ]

        self.env["UNION_MODEL_LOADER_LOCAL_MODEL_PATH"] = "/root/union"

        stream_model_str = "true" if self.stream_model else "false"
        self.env["UNION_MODEL_LOADER_STREAM_SAFETENSORS"] = stream_model_str

        super().__post_init__()
