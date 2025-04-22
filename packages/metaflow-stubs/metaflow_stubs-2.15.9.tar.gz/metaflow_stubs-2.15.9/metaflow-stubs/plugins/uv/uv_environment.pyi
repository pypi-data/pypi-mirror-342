######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.9                                                                                 #
# Generated on 2025-04-22T01:36:50.286573                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.exception
    import metaflow.metaflow_environment

from ...exception import MetaflowException as MetaflowException

class UVException(metaflow.exception.MetaflowException, metaclass=type):
    ...

class UVEnvironment(metaflow.metaflow_environment.MetaflowEnvironment, metaclass=type):
    def __init__(self, flow):
        ...
    def validate_environment(self, logger, datastore_type):
        ...
    def init_environment(self, echo, only_steps = None):
        ...
    def executable(self, step_name, default = None):
        ...
    def add_to_package(self):
        ...
    def pylint_config(self):
        ...
    def bootstrap_commands(self, step_name, datastore_type):
        ...
    ...

