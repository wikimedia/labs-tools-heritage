#!/usr/bin/env python
"""Parse Git logs of the latest deploy and prepare a SAL message."""

import re
import subprocess

GIT_COMMIT_FIELDS = ['id', 'message']
GIT_LOG_FORMAT_FIELDS = ['%h', '%b']
GIT_LOG_FORMAT = '%x1f'.join(GIT_LOG_FORMAT_FIELDS) + '%x1e'
GIT_LOG_OPTIONS = '@{1}.. --reverse -C --no-merges'


def get_git_log():
    """Run git log on the Shell and parse the output."""
    command = 'git log %s --format="%s"' % (GIT_LOG_OPTIONS, GIT_LOG_FORMAT)
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    (log, _) = process.communicate()
    log = log.decode('utf-8').strip('\n\x1e').split('\x1e')
    log = [row.strip().split('\x1f') for row in log]
    log = [dict(list(zip(GIT_COMMIT_FIELDS, row))) for row in log]
    return log


def update_with_task_name(log_entry):
    """Update the current log-entry with the mentioned task names (if exists)."""
    tasks = search_for_tasks(log_entry['message'])
    log_entry['tasks'] = tasks
    return log_entry


def search_for_tasks(message):
    """Return all task IDs mentioned in the message."""
    pattern = re.compile(r'(?:^|\n)Bug: (T\d+)', re.M)
    return re.findall(pattern, message)


def format_entry(log_entry):
    """Format a git log entry to our deploy message format."""
    if log_entry['tasks']:
        return '%s (%s)' % (log_entry['id'], ', '.join(log_entry['tasks']))
    else:
        return log_entry['id']


def format_update_for_dologmsg(structured_log):
    """Return a post-deploy message for dologmsg from the structured log."""
    commits = ', '.join([format_entry(x) for x in structured_log])
    return 'Deploy {}'.format(commits)


def main():
    log = get_git_log()
    augmented_log = [update_with_task_name(x) for x in log]
    print(format_update_for_dologmsg(augmented_log))


if __name__ == '__main__':
    main()
