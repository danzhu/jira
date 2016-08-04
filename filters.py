#!/usr/bin/python

from datetime import datetime, timedelta

from display import display
import config

STATUS    = '{fore.CYAN}{issue.status!s:<10}{fore.RESET}'
ISSUETYPE = '{style.BRIGHT}{fore.BLUE}{issue.issuetype!s:<10}{style.RESET_ALL}'
PRIORITY  = '{fore.MAGENTA}{issue.priority!s:<10}{fore.RESET}'
UPDATED   = '{fore.BLUE}{issue.updated:%d %I:%M  }{fore.RESET}'
ASSIGNEE  = '{style.BRIGHT}{fore.CYAN}{issue.assignee!s:<10}{style.RESET_ALL}'
SUMMARY   = '{issue.summary}'


class Filter:
    NAME       = 'Filter'
    FORMAT     = STATUS + ISSUETYPE + PRIORITY + UPDATED + ASSIGNEE + SUMMARY
    REVERSE    = True
    HIDE_EMPTY = True

    def update(self, issues):
        self.matches = [i for i in issues if self.filter(i)]

        displays = [i for i in self.matches if self.detail(i)]
        self.displays = sorted(displays, key=self.sort, reverse=self.REVERSE)

    def display(self):
        if self.HIDE_EMPTY and len(self.matches) == 0:
            return

        display(config.TITLE_FORMAT, name=self.NAME, count=len(self.matches))

        if len(self.displays) == 0:
            return

        for issue in self.displays:
            display(config.PREFIX_FORMAT + self.FORMAT, issue=issue, browse=config.URL + 'browse/')

        display()

    def sort(self, issue):
        return issue.updated

    def filter(self, i):
        return True

    def detail(self, i):
        return True


class Action(Filter):
    NAME = 'Action Needed'
    FORMAT = STATUS + SUMMARY

    def filter(self, i):
        return i.status in ['Merge Needed', 'Development - Passed Review'] and i.assigned

    def sort(self, issue):
        return issue.status


class Progress(Filter):
    NAME = 'In Progress'
    FORMAT = UPDATED + SUMMARY

    def filter(self, i):
        return i.status in ['Development - In Progress'] and i.assigned

    def sort(self, issue):
        return issue.lastViewed


class Open(Filter):
    NAME = 'Open'
    FORMAT = PRIORITY + SUMMARY

    def filter(self, i):
        return i.status in ['Development - Open'] and i.assigned

    def sort(self, issue):
        return issue.priority


class Estimate(Filter):
    NAME = 'Estimate'
    FORMAT = ISSUETYPE + SUMMARY

    def filter(self, i):
        return i.status in ['Estimate'] and i.assigned

    def sort(self, issue):
        return issue.status


class Pending(Filter):
    NAME = 'Pending'
    FORMAT = STATUS + SUMMARY

    def filter(self, i):
        if i.status in [
                'QA Smoke Test',
                'Done'
                ]:
            return False

        # if either unassigned or assigned to someone else
        if i.assigned != True:
            return True

        # or assigned to me but not in these status
        return i.status not in [
                'Estimate',
                'Development - Open',
                'Development - In Progress',
                'Development - Passed Review',
                'Merge Needed'
                ]


class Smoke(Filter):
    NAME = 'Smoke Test'
    FORMAT = ASSIGNEE + SUMMARY

    def filter(self, i):
        return i.status in ['QA Smoke Test']

    def detail(self, i):
        return i.updated > i.lastViewed


class Total(Filter):
    NAME = 'Total'
    HIDE_EMPTY = False

    def detail(self, i):
        return False


filters = [Action(), Progress(), Open(), Estimate(), Pending(), Smoke(), Total()]
