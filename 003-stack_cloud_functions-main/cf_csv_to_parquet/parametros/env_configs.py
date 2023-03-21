import logging
import os
import sys

from parametros.logger import logger


class EnvConfigs:
    def __init__(self):
        self.environment_configs = os.environ
        self.expected_envs = [
            "GCP_PROJECT",
            "BUCKET_RAW",
            "BUCKET_HIST"
        ]
        self.validate()

    def validate(self):
        for env in self.expected_envs:
            if env not in os.environ.keys():
                logger.error(f'Please set the environment variable {env}')
                sys.exit(1)

    def get_gcp_project(self):
        return self.environment_configs.get("GCP_PROJECT")

    def get_bucket_source(self):
        return self.environment_configs.get("BUCKET_RAW")

    def get_bucket_destination(self):
        return self.environment_configs.get("BUCKET_HIST")

