# Copyright (c) 2021 by Apex.AI Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0

import os

import unittest

import launch
from launch_ros.substitutions import ExecutableInPackage
import launch_testing
import launch_testing.actions
from launch_testing.asserts import assertSequentialStdout

import pytest


@pytest.mark.launch_test
def generate_test_description():

    proc_env = os.environ.copy()
    colcon_prefix_path = os.environ.get('COLCON_PREFIX_PATH', '')
    executable_list = ['iox-ex-waitset-publisher', 'iox-ex-waitset-gateway',
                       'iox-ex-waitset-grouping', 'iox-ex-waitset-individual',
                       'iox-ex-waitset-sync', 'iox-ex-waitset-trigger']
    process_list = []

    for exec in executable_list:
        tmp_exec = os.path.join(
            colcon_prefix_path,
            'example_waitset/bin/',
            exec)
        tmp_process = launch.actions.ExecuteProcess(
            cmd=[tmp_exec],
            env=proc_env, output='screen')
        process_list.append(tmp_process)

    print("Process list:", process_list)

    roudi_executable = ExecutableInPackage(
        package='iceoryx_integrationtest', executable='iox-roudi')
    roudi_process = launch.actions.ExecuteProcess(
        cmd=[roudi_executable, '-l', 'debug'],
        env=proc_env, output='screen',
        sigterm_timeout='20'
    )

    return launch.LaunchDescription([
        process_list[0],
        process_list[1],
        process_list[2],
        process_list[3],
        process_list[4],
        roudi_process,
        launch_testing.actions.ReadyToTest()
    ]), {'iox-ex-waitset-publisher': process_list[0], 'iox-ex-waitset-gateway': process_list[1],
         'iox-ex-waitset-grouping': process_list[2], 'iox-ex-waitset-individual': process_list[3],
         'iox-ex-waitset-sync': process_list[4], 'roudi_process': roudi_process}


class TestWaitSetExample(unittest.TestCase):
    def test_roudi_ready(self, proc_output):
        proc_output.assertWaitFor(
            'RouDi is ready for clients', timeout=45, stream='stdout')

    def test_waitset_publisher(self, proc_output):
        proc_output.assertWaitFor(
            'Sending: 10', timeout=45, stream='stdout')

    def test_waitset_grouping(self, proc_output):
        proc_output.assertWaitFor(
            'dismiss data', timeout=45, stream='stdout')
        proc_output.assertWaitFor(
            'received: 10', timeout=45, stream='stdout')

    def test_waitset_individual(self, proc_output):
        proc_output.assertWaitFor(
            'subscriber 2 received something - dont care', timeout=45, stream='stdout')
        proc_output.assertWaitFor(
            'subscriber 1 received: 10', timeout=45, stream='stdout')

    def test_waitset_sync(self, proc_output):
        proc_output.assertWaitFor(
            'activation callback', timeout=45, stream='stdout')


@ launch_testing.post_shutdown_test()
class TestWaitSetExampleExitCodes(unittest.TestCase):
    def test_exit_code(self, proc_info):
        launch_testing.asserts.assertExitCodes(proc_info)
