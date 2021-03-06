# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""service-management delete command."""

from googlecloudsdk.api_lib.endpoints import services_util
from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.endpoints import arg_parsers
from googlecloudsdk.command_lib.endpoints import common_flags
from googlecloudsdk.core.console import console_io


class Delete(base.DeleteCommand):
  # pylint: disable=line-too-long
  """Deletes a service from Google Service Management.

     Services that are deleted will be retained in the system for 30 days.
     If a deleted service is still within this retention window, it can be
     undeleted with the undelete command.

     ## EXAMPLES
     To delete a service named `my-service`, run:

       $ {command} my-service

     To run the same command asynchronously (non-blocking), run:

       $ {command} my-service --async
  """
  # pylint: enable=line-too-long

  @staticmethod
  def Args(parser):
    """Args is called by calliope to gather arguments for this command.

    Args:
      parser: An argparse parser that you can use to add arguments that go
          on the command line after this command. Positional arguments are
          allowed.
    """
    common_flags.producer_service_flag(suffix='to delete').AddToParser(parser)

    base.ASYNC_FLAG.AddToParser(parser)
    parser.display_info.AddCacheUpdater(None)

  def Run(self, args):
    """Run 'service-management delete'.

    Args:
      args: argparse.Namespace, The arguments that this command was invoked
          with.

    Returns:
      The response from the Delete API call (or None if cancelled).
    """
    messages = services_util.GetMessagesModule()
    client = services_util.GetClientInstance()

    # Prompt with a warning before continuing.
    console_io.PromptContinue(
        message='Are you sure? This will set the service configuration to be '
        'deleted, along with all of the associated consumer '
        'information. Note: This does not immediately delete the '
        'service configuration or data and can be undone using the '
        'undelete command for 30 days. Only after 30 days will the '
        'service be purged from the system.',
        prompt_string='Continue anyway',
        default=True,
        throw_if_unattended=True,
        cancel_on_no=True)

    service = arg_parsers.GetServiceNameFromArg(args.service)

    request = messages.ServicemanagementServicesDeleteRequest(
        serviceName=service,)

    operation = client.services.Delete(request)

    return services_util.ProcessOperationResult(operation, args.async)
