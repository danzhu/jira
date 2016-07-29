#!/usr/bin/python

from functools import total_ordering
from colorama import Fore, Back, Style

from display import display
from helpers import parseTime, tryCall

FIELDS = 'key,summary,priority,issuetype,status,assignee,updated,lastViewed,description'


class Issue:
    def __init__(self, json, user):
        self.json = json

        self.key = json['key']

        fields = json['fields']
        self.summary     = str(fields['summary'])
        self.description = str(fields['description'])
        self.priority    = Priority(fields['priority'])
        self.issuetype   = IssueType(fields['issuetype'])
        self.status      = Status(fields['status'])
        self.assignee    = tryCall(User, fields['assignee'])
        self.updated     = parseTime(fields['updated'])
        self.lastViewed  = parseTime(fields['lastViewed'])

        if self.assignee is None:
            self.assigned = None
        elif self.assignee.name == user:
            self.assigned = True
        else:
            self.assigned = False

        if self.lastViewed is None:
            self.sign = '+'
        elif self.updated > self.lastViewed:
            self.sign = '*'
        else:
            self.sign = ' '

        #self.comments   = [Comment(c) for c in json['comment']['comments']]

@total_ordering
class Priority:
    def __init__(self, json):
        self.id   = int(json['id'])
        self.name = str(json['name'])

    def __str__(self):
        return self.name

    def __eq__(self, other):
        if type(other) == str:
            return self.name == other
        elif type(other) == int:
            return self.id == other
        elif type(other) == Priority:
            return self.id == other.id
        else:
            return False

    def __lt__(self, other):
        return self.id > other.id


@total_ordering
class Status:
    ABBREV = {
            1:     '    Open', # Open
            10029: '    Done', # Done
            10032: '    MeNe', # Merge Needed
            10332: 'Dev CoRe', # Development - Code Review
            10333: 'Dev PaRe', # Development - Passed Review
            10334: 'QA  Open', # QA - Open
            10335: 'QA  InPr', # QA - In Progress
            10337: 'QA  Appr', # QA - Approved
            10426: '    Esti', # Estimate
            10427: 'Dev Open', # Development - Open
            10428: 'Dev InPr', # Development - In Progress
            10429: 'QA  SmTe'  # QA Smoke Test
            }

    def __init__(self, json):
        self.id          = int(json['id'])
        self.name        = str(json['name'])
        self.description = str(json['description'])

    def __str__(self):
        return Status.ABBREV.get(self.id, '{0.id} {0.name}'.format(self))

    def __eq__(self, other):
        if type(other) == str:
            return self.name == other
        elif type(other) == int:
            return self.id == other
        elif type(other) == Status:
            return self.id == other.id
        else:
            return False

    def __lt__(self, other):
        return self.id < other.id


@total_ordering
class User:
    def __init__(self, json):
        self.displayName  = str(json['displayName'])
        self.name         = str(json['name'])
        self.emailAddress = str(json['emailAddress'])
        self.active       = str(json['active'])

    def __str__(self):
        # first name only
        return self.displayName[:self.displayName.index(' ')]

    def __eq__(self, other):
        if type(other) == str:
            return self.name == other or self.displayName == other
        elif type(other) == User:
            return self.name == other.name
        else:
            return False

    def __lt__(self, other):
        return self.name < other.name


@total_ordering
class IssueType:
    ABBREV = {
            1: 'Bug     ', # Bug
            2: 'Feature ', # New Feature
            3: 'Task    ', # Task
            4: 'Improve '  # Improvement
            }
    def __init__(self, json):
        self.id      = int(json['id'])
        self.name    = str(json['name'])
        self.subtask = str(json['subtask'])

    def __str__(self):
        return IssueType.ABBREV.get(self.id, self.name)

    def __eq__(self, other):
        if type(other) == str:
            return self.name == other
        elif type(other) == int:
            return self.id == other
        elif type(other) == IssueType:
            return self.id == other.id
        else:
            return False

    def __lt__(self, other):
        return self.id < other.id


@total_ordering
class Comment:
    def __init__(self, json):
        self.id           = int(json['id'])
        self.body         = json['body']
        self.author       = tryCall(User, json['author'])
        self.updateAuthor = tryCall(User, json['updateAuthor'])
        self.created      = parseTime(json['created'])
        self.updated      = parseTime(json['updated'])

    def __str__(self):
        return self.body

    def __eq__(self, other):
        if type(other) == int:
            return self.id == other
        if type(other) == Comment:
            return self.id == other.id
        else:
            return False

    def __lt__(self, other):
        return self.id < other.id
