*** Settings ***
Library  RequestsLibrary
Library  Collections

*** Keywords ***


send_post
    [Arguments]    ${uri}    ${ParameterDict}    ${DataType}    ${header}
    [Documentation]    不创建会话，仅发送post请求；
    ...    响应数据为json类型
    ${RequestData}    Create Dictionary
    log    ${ParameterDict.keys()}
    : FOR    ${key}    IN    @{ParameterDict.keys()}
    \    set to dictionary    ${RequestData}    ${key}    ${ParameterDict['${key}']}
    log    ${RequestData}
    create session    postHttp    ${uri}
    ${response}    post on session   postHttp    ${uri}    ${DataType}=${RequestData}    headers=${header}    timeout=${timeout}
    ${ResponseBody}    To Json    ${response.content}
    sleep    2s
    log    ${response.text}
    [Return]    ${response}

send_get
    [Arguments]    ${uri}    ${ParameterDict}    ${header}  ${timeout}
    [Documentation]    不创建会话，仅发送get请求；
    ...    响应数据为json类型
    ${RequestData}    Create Dictionary
    log    ${ParameterDict.keys()}
    FOR  ${key}  IN   @{ParameterDict.keys()}
        set to dictionary   ${RequestData}    ${key}    ${ParameterDict['${key}']}
    END
    log    ${RequestData}
    create session    getHttp    ${uri}
    ${response}=  GET On Session  getHttp  ${uri}  params=${RequestData}  headers=${header}   timeout=${timeout}
    ${ResponseBody}  To Json  ${response.content}
    sleep  2s
    log    ${response.text}
    [Return]    ${ResponseBody}

