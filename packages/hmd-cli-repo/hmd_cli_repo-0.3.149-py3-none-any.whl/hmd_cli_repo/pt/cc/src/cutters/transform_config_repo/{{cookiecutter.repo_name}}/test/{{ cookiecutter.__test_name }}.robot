*** Settings ***
Library           BuiltIn
Library           hmd_lib_robot_shared.transform_client_robot_lib.TransformLib    ${transform_instance_name}    hmd-ms-transform    ${HMD_DID}    ${HMD_ENVIRONMENT}    ${HMD_REGION}    ${HMD_CUSTOMER_CODE}    ${HMD_ACCOUNT}
Variables         vars.py

*** Variables ***

*** Test Cases ***
Example Test
    No Operation
