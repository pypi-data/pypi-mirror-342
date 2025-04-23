import os

from dotenv import load_dotenv

from mcp_server_tls.consts import *

class TlsConfig:

    ak: str
    sk: str
    region: str
    endpoint: str
    token: str
    project_id: str
    account_id: str
    enabled_tools: list

    def __init__(self):
        self.ak = os.getenv("AK") or os.getenv("VOLC_ACCESSKEY")
        self.sk = os.getenv("SK") or os.getenv("VOLC_SECRETKEY")
        self.region = os.getenv("REGION")
        self.endpoint = os.getenv("ENDPOINT")
        self.token = os.getenv("TOKEN", "")
        self.project_id = os.getenv("PROJECT_ID")
        self.topic_id = os.getenv("TOPIC_ID")
        self.account_id = os.getenv("ACCOUNT_ID")

        self.deploy_mode = os.getenv("DEPLOY_MODE", DEPLOY_MODE_LOCAL)
        self.enabled_tools = os.getenv("ENABLED_TOOLS", "all").split(",")

        self._validate()

    def _validate(self):
        self._validate_region()
        self._validate_endpoint()
        self._validate_deploy_mode()
        self._validate_deploy_mode_dependencies()

    def _validate_ak(self):
        if not self.ak:
            raise ValueError("environment variables AK is required")

    def _validate_sk(self):
        if not self.sk:
            raise ValueError("environment variables SK is required")

    def _validate_region(self):
        if not self.region:
            raise ValueError("environment variables REGION is required")

    def _validate_deploy_mode(self):
        if self.deploy_mode not in (DEPLOY_MODE_LOCAL, DEPLOY_MODE_REMOTE):
            raise ValueError("environment variables DEPLOY_MODE should be {} or {}".format(DEPLOY_MODE_LOCAL, DEPLOY_MODE_REMOTE))

    def _validate_endpoint(self):
        if not self.endpoint:
            raise ValueError("environment variables ENDPOINT is required")
        if not (self.endpoint.startswith("http://") or self.endpoint.startswith("https://")):
            raise ValueError(f"Invalid environment variables endpoint: {self.endpoint}. It must start with 'http://' or 'https://'.")

    def _validate_deploy_mode_dependencies(self):
        if self.deploy_mode == DEPLOY_MODE_LOCAL:
            self._validate_ak()
            self._validate_sk()
        else:
            self._validate_deploy_mode_remote_should_not_exist()

    def _validate_deploy_mode_remote_should_not_exist(self):
        if self.ak:
            raise ValueError("environment variables AK or VOLC_ACCESSKEY should not be set")
        if self.sk:
            raise ValueError("environment variables SK or VOLC_SECRETKEY should not be set")
        if self.token:
            raise ValueError("environment variables TOKEN should not be set")
        if self.project_id:
            raise ValueError("environment variables PROJECT_ID should not be set")
        if self.topic_id:
            raise ValueError("environment variables TOPIC_ID should not be set")
        if self.account_id:
            raise ValueError("environment variables ACCOUNT_ID should not be set")

load_dotenv()

TLS_CONFIG = TlsConfig()