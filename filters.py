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
    NAME = 'Filter'
    FORMAT = STATUS + ISSUETYPE + PRIORITY + UPDATED + ASSIGNEE + SUMMARY
    REVERSE = True

    def update(self, issues):
        self.matches = [i for i in issues if self.filter(i)]
        self.matches.sort(key=self.sort, reverse=self.REVERSE)

    def display(self):
        if len(self.matches) == 0:
            return

        display(config.TITLE_FORMAT, name=self.NAME, count=len(self.matches))

        for issue in self.matches:
            display(config.PREFIX_FORMAT + self.FORMAT, issue=issue, browse=config.URL + 'browse/')

    def filter(self, i):
        return True

    def sort(self, issue):
        return issue.updated


class Action(Filter):
    NAME = 'Action Needed'
    FORMAT = STATUS + SUMMARY

    def filter(self, i):
        return i.status in ['Merge Needed', 'Development - Passed Review']

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
                'Development - Passed Review',
                'Merge Needed',
                'Done'
                ]:
            return False

        if i.assigned != True:
            return True

        return i.status not in [
                'Estimate',
                'Development - Open',
                'Development - In Progress'
                ]


class Done(Filter):
    NAME = 'Done'

    def display(self):
        # don't display actual issues, just number of matches
        # (don't ignore 0 length either)
        display(config.TITLE_FORMAT, name=self.NAME, count=len(self.matches))

    def filter(self, i):
        return i.status in ['Done']


filters = [Action(), Progress(), Open(), Estimate(), Pending()]
