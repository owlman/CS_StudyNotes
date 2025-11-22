*** Settings ***
Library           Selenium2Library

*** Test Cases ***
openBaiduCase
    Open Browser    http://www.baidu.com
    Input Text    id=kw    robot framework
    Click Button    id=su
    Sleep    5
    Close Browser
