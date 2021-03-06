# Copyright 2018 Google Inc. All Rights Reserved.
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
"""`gcloud monitoring policies conditions describe` command."""
from googlecloudsdk.api_lib.monitoring import policies
from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.monitoring import resource_args
from googlecloudsdk.command_lib.monitoring import util


class Describe(base.CreateCommand):
  """Describe a condition in a Stackdriver alerting policy."""

  @staticmethod
  def Args(parser):
    condition_arg = resource_args.CreateConditionResourceArg(
        'describe')
    resource_args.AddResourceArgs(parser, [condition_arg])

  def Run(self, args):
    client = policies.AlertPolicyClient()
    condition_ref = args.CONCEPTS.condition.Parse()
    policy_ref = condition_ref.Parent()
    policy = client.Get(policy_ref)

    condition = util.GetConditionFromPolicy(condition_ref.RelativeName(),
                                            policy)

    return condition
