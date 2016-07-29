#!/usr/bin/python

from getpass import getpass
from datetime import datetime
import requests
import operator
import subprocess
import os
import json

from issue import Issue, FIELDS
from filters import filters
from display import init, display, error
import config

# global variables
issues   = []
password = None
updated  = None

# send request to JIRA API
def request(action):
    global password

    if password is None:
        display('\nUsername: {}', config.USER)
        try:
            password = getpass()
        except KeyboardInterrupt:
            display()
            return None

    url = '{}rest/api/2/{}'.format(config.URL, action)

    try:
        r = requests.get(url,
                auth=(config.USER, password),
                headers={'Content-Type': 'application/json'},
                timeout=config.TIMEOUT)
    except requests.exceptions.Timeout:
        error('Request timed out after {} seconds', config.TIMEOUT)
        return None

    if r.status_code == requests.codes.ok:
        return r.json()

    elif r.status_code == requests.codes.unauthorized:
        error('Unable to authenticate. Please re-enter your password')
        password = None
        return None

    elif r.status_code == requests.codes.forbidden:
        error('API login revoked. Please re-login on JIRA website and complete the CAPTCHA')
        subprocess.call([config.BROWSER, config.URL])
        return None

    else:
        try:
            data = r.json()
            error('Response status {}: {}', r.status_code, data['errorMessages'][0])
        except ValueError:
            error('Response status {}', r.status_code)

        return None

def do(action, args=''):
    global issues, updated

    if action == '':
        action = config.DEFAULT_ACTION

    if action == 'update':
        data = request('search?jql={}&fields={}'.format(
            config.QUERY.replace(' ', '+'), FIELDS))

        if data is None:
            return

        issues = [Issue(it, config.USER) for it in data['issues']]

        for fil in filters:
            fil.update(issues)
            fil.display()

        updated = datetime.today()
        display(config.SUMMARY_FORMAT, total=len(issues), updated=updated)

    elif action == 'print':
        if updated is None:
            display('No data available')
            return

        for fil in filters:
            fil.display()

        display(config.SUMMARY_FORMAT, total=len(issues), updated=updated)

    elif action == 'display':
        issue = findIssue(args)
        if issue is not None:
            display(config.DETAILS_FORMAT, issue=issue)
        else:
            error('Issue "{}" not found in cache', key)

    elif action == 'open':
        key = default(args)
        url = '{}browse/{}'.format(config.URL, key)
        display('Opening {}', url)
        subprocess.call([config.BROWSER, url])

    elif action == 'json':
        issue = findIssue(args)
        data = json.dumps(issue.json, indent=4, separators=(',', ': '))
        display('JSON source for issue "{}":\n{}', issue.key, data)

    elif action == 'get':
        data = request(args)

        if data is None:
            return

        display('GET request result:\n{}',
                json.dumps(data, indent=4, separators=(',', ': ')))

    elif action == 'help':
        error('No help available')

    elif action == 'crash':
        raise RuntimeError('Oops. Crashed.')

    else:
        script = 'scripts\\{}.bat'.format(action)
        if not os.path.isfile(script):
            error('Not a script or command: {}', action)
            return

        exitCode = subprocess.call(script + ' ' + args, shell=True)
        if exitCode != 0:
            display('Exit code {}', exitCode)

def default(args):
    if args != '':
        return config.KEY_PREFIX + args

    if len(issues) > 0:
        return issues[0].key

    return None

def findIssue(args):
    if args != '':
        key = config.KEY_PREFIX + args
        return next((i for i in issues if i.key == key), None)

    if len(issues) > 0:
        return issues[0]

    return None

def main():
    init()

    if config.STARTUP_ACTION is not None:
        do(config.STARTUP_ACTION)

    while True:
        display('')

        try:
            command = input('> ')
        except KeyboardInterrupt:
            continue
        except EOFError:
            break

        if command == 'exit':
            break
        if command == 'restart':
            exit(2)

        idx = command.find(' ')
        if idx >= 0:
            do(command[:idx], command[idx + 1:])
        else:
            do(command)

if __name__ == '__main__':
    main()
