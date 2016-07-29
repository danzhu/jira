#!/usr/bin/python

# user settings
USER           = 'danzh'
KEY_PREFIX     = 'WEB-'
BROWSER        = 'chrome'
DEFAULT_ACTION = 'update'
STARTUP_ACTION = 'update'

# request settings
URL     = 'http://jira:8080/'
QUERY   = 'assignee was "Daniel Zhu" and status not in (Done) order by updated'
TIMEOUT = 20

# default display formats
DETAILS_FORMAT = """
{fore.GREEN}{issue.key:<12}{fore.RESET}{issue.summary}

{fore.YELLOW}Type:       {fore.RESET}{issue.issuetype}
{fore.YELLOW}Priority:   {fore.RESET}{issue.priority}
{fore.YELLOW}Assignee:   {fore.RESET}{issue.assignee}
{fore.YELLOW}Status:     {fore.RESET}{issue.status.name}

{issue.description}
"""
TITLE_FORMAT  = '\n{style.BRIGHT}{fore.YELLOW}{name}: {style.RESET_ALL}{count}'
PREFIX_FORMAT = '{style.BRIGHT}{fore.BLACK}{browse}{fore.GREEN}{issue.key:<10}{fore.RED}{issue.sign}{style.RESET_ALL}  '
SUMMARY_FORMAT = """
Total: {total}
Updated: {updated:%I:%M %p}
"""
