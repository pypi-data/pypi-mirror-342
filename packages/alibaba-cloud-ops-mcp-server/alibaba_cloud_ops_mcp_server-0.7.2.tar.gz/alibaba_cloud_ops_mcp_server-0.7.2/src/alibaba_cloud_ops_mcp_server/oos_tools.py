from pydantic import Field
from typing import List
import os
import json
import time

from alibabacloud_oos20190601.client import Client as oos20190601Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_oos20190601 import models as oos_20190601_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient


END_STATUSES = ['Success', 'Failed', 'Cancelled']


tools = []

def create_client(region_id: str) -> oos20190601Client:
    config = open_api_models.Config(
        access_key_id=os.environ['ALIBABA_CLOUD_ACCESS_KEY_ID'],
        access_key_secret=os.environ['ALIBABA_CLOUD_ACCESS_KEY_SECRET'],
        user_agent='alibaba-cloud-ops-mcp-server',
    )
    config.endpoint = f'oos.{region_id}.aliyuncs.com'
    return oos20190601Client(config)


def _start_execution_sync(region_id: str, template_name: str, parameters: dict):
    client = create_client(region_id=region_id)
    start_execution_request = oos_20190601_models.StartExecutionRequest(
        region_id=region_id,
        template_name=template_name,
        parameters=json.dumps(parameters)
    )
    start_execution_resp = client.start_execution(start_execution_request)
    execution_id = start_execution_resp.body.execution.execution_id

    while True:
        list_executions_request = oos_20190601_models.ListExecutionsRequest(
            region_id=region_id,
            execution_id=execution_id
        )
        list_executions_resp = client.list_executions(list_executions_request)
        status = list_executions_resp.body.executions[0].status
        if status in END_STATUSES:
            return list_executions_resp.body
        time.sleep(1)
@tools.append
def RunCommand(
     RegionId: str = Field(description='AlibabaCloud region ID', default='cn-hangzhou'),
     InstanceIds: List[str] = Field(description='AlibabaCloud ECS instance ID List'),
     CommandType: str = Field(description='ECS实例上执行的命令类型，可选值：RunShellScript，RunPythonScript，RunPerlScript，RunBatScript，RunPowerShellScript', default='RunShellScript'),
     Command: str = Field(description='ECS实例上执行的命令内容'),
):
    """批量在多台ECS实例上运行云助手命令，适用于需要同时管理多台ECS实例的场景，如应用程序管理和资源标记操作等。"""
    
    parameters = {
        'regionId': RegionId,
        'resourceType': 'ALIYUN::ECS::Instance',
        'targets': {
            'ResourceIds': InstanceIds,
            'RegionId': RegionId,
            'Type': 'ResourceIds',
            'Parameters': {
                'RegionId': RegionId,
                'Status': 'Running'
            }
        },
        "commandType": CommandType,
        "commandContent": Command
    }
    return _start_execution_sync(region_id=RegionId, template_name='ACS-ECS-BulkyRunCommand', parameters=parameters)
    

@tools.append
def StartInstances(
     RegionId: str = Field(description='AlibabaCloud region ID', default='cn-hangzhou'),
     InstanceIds: List[str] = Field(description='AlibabaCloud ECS instance ID List'),
):
    """批量启动ECS实例，适用于需要同时管理和启动多台ECS实例的场景，例如应用部署和高可用性场景。"""
    
    parameters = {
        'regionId': RegionId,
        'resourceType': 'ALIYUN::ECS::Instance',
        'targets': {
            'ResourceIds': InstanceIds,
            'RegionId': RegionId,
            'Type': 'ResourceIds'
        }
    }
    return _start_execution_sync(region_id=RegionId, template_name='ACS-ECS-BulkyStartInstances', parameters=parameters)


@tools.append
def StopInstances(
     RegionId: str = Field(description='AlibabaCloud region ID', default='cn-hangzhou'),
     InstanceIds: List[str] = Field(description='AlibabaCloud ECS instance ID List'),
     ForeceStop: bool = Field(description='是否强制关机', default=False),
):
    """批量停止ECS实例，适用于需要同时管理和停止多台ECS实例的场景。"""
    
    parameters = {
        'regionId': RegionId,
        'resourceType': 'ALIYUN::ECS::Instance',
        'targets': {
            'ResourceIds': InstanceIds,
            'RegionId': RegionId,
            'Type': 'ResourceIds'
        },
        'forceStop': ForeceStop
    }
    return _start_execution_sync(region_id=RegionId, template_name='ACS-ECS-BulkyStopInstances', parameters=parameters)


@tools.append
def RebootInstances(
     RegionId: str = Field(description='AlibabaCloud region ID', default='cn-hangzhou'),
     InstanceIds: List[str] = Field(description='AlibabaCloud ECS instance ID List'),
     ForeceStop: bool = Field(description='是否强制关机', default=False),
):
    """批量重启ECS实例，适用于需要同时管理和重启多台ECS实例的场景。"""
    
    parameters = {
        'regionId': RegionId,
        'resourceType': 'ALIYUN::ECS::Instance',
        'targets': {
            'ResourceIds': InstanceIds,
            'RegionId': RegionId,
            'Type': 'ResourceIds'
        },
        'forceStop': ForeceStop
    }
    return _start_execution_sync(region_id=RegionId, template_name='ACS-ECS-BulkyRebootInstances', parameters=parameters)


@tools.append
def RunInstances(
    RegionId: str = Field(description='AlibabaCloud region ID', default='cn-hangzhou'),
    ImageId: str = Field(description='镜像ID'),
    InstanceType: str = Field(description='实例规格'),
    SecurityGroupId: str = Field(description='安全组ID'),
    VSwitchId: str = Field(description='交换机ID'),
    Amount: int = Field(description='创建数量', default=1),
    InstanceName: str = Field(description='实例名称', default=''),
):
    """批量创建ECS实例，适用于需要同时创建多台ECS实例的场景，例如应用部署和高可用性场景。"""

    parameters = {
        'imageId': ImageId,
        'instanceType': InstanceType,
        'securityGroupId': SecurityGroupId,
        'vSwitchId': VSwitchId,
        'amount': Amount,
        'instanceName': InstanceName
    }
    return _start_execution_sync(region_id=RegionId, template_name='ACS-ECS-RunInstances', parameters=parameters)


@tools.append
def ResetPassword(
    RegionId: str = Field(description='AlibabaCloud region ID', default='cn-hangzhou'),
    InstanceIds: List[str] = Field(description='AlibabaCloud ECS instance ID List'),
    Password: str = Field(description='ECS实例的密码,8-30个字符且只能包含以下限制条件中的字符：小写字母，大写字母，数字，只可包含特殊字符（）~！@#$%^&*-_+=（40：<>，？/'),
):
    """批量修改ECS实例的密码，请注意，本操作将会重启ECS实例"""
    parameters = {
        'regionId': RegionId,
        'resourceType': 'ALIYUN::ECS::Instance',
        'targets': {
            'ResourceIds': InstanceIds,
            'RegionId': RegionId,
            'Type': 'ResourceIds'
        },
        'password': Password
    }
    return _start_execution_sync(region_id=RegionId, template_name='ACS-ECS-BulkyResetPassword', parameters=parameters)

@tools.append
def ReplaceSystemDisk(
        RegionId: str = Field(description='AlibabaCloud region ID', default='cn-hangzhou'),
        InstanceIds: List[str] = Field(description='AlibabaCloud ECS instance ID List'),
        ImageId: str = Field(description='镜像ID')
):
    """批量替换ECS实例的系统盘，更换操作系统"""
    parameters = {
        'regionId': RegionId,
        'resourceType': 'ALIYUN::ECS::Instance',
        'targets': {
            'ResourceIds': InstanceIds,
            'RegionId': RegionId,
            'Type': 'ResourceIds'
        },
        'imageId': ImageId
    }
    return _start_execution_sync(region_id=RegionId, template_name='ACS-ECS-BulkyReplaceSystemDisk', parameters=parameters)
