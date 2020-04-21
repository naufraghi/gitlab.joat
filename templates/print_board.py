#!/usr/bin/python

import os
import math
import json

END = '\033[0m'
BOLD = '\033[1m'
RED = '\033[91m'
BLUE = '\033[36m'

default_label_map = {
    'Feature': '🚀',
    'Bug': '🐛',
    'Tech improvement': '🤖',
    'Requirement work': '📝',
    'Improvement': '🎨',
    'Tech support task': '🔧',
    'Sub-task': '🍕',
}
default_unknown_label_emoji = os.environ.get(
    'DEFAULT_UNKNOWN_LABEL_EMOJI', '🤔')

env_label_map = os.environ.get('LABEL_MAP', None)
label_map = json.loads(env_label_map) if env_label_map else default_label_map


def get_text_red(text):
    return '{}{}{}'.format(RED, text, END)


def get_text_bold(text):
    return '{}{}{}'.format(BOLD, text, END)


def get_ticket_number(issue):
    number = str(issue['iid'])[-4:]
    return f"{number} "


def get_assignee(issue):
    try:
        assignee = issue['assignees'][0]
        name = assignee['name']
        initials = name[:2].upper()
        return f"({initials}) "
    except IndexError:
        return ' ' * 5


def get_issue_type(issue):
    labels = issue['labels']
    for (label, emoji) in label_map.items():
        if label in labels:
            return emoji
    return default_unknown_label_emoji


def demux_issues(issues, columns):
    issues_lists = []
    for column in columns:
        issues_lists.append(
            [issue for issue in issues if column in issue['labels']]
        )
    return issues_lists


def get_rows(issues, columns, icw, separator):
    issues_lists = demux_issues(issues, columns)
    no_rows = len(max(issues_lists, key=len))
    rows = []
    for i in range(0, no_rows):
        row = ''
        for j, column in enumerate(columns):
            sep = separator if column != columns[-1] else ''
            try:
                issue = issues_lists[j][i]
                title = issue['title']
                number = get_ticket_number(issue)
                assignee = get_assignee(issue)
                issue_type = f"{get_issue_type(issue)} "
                title_size = \
                    icw - len(number) - len(assignee) - len(issue_type) - 1
                if title_size <= 0:
                    return 'TERMINAL TOO SMALL'
                number_b = get_text_bold(number)
                assignee_r = get_text_red(assignee)
                row += f"{number_b}{assignee_r}{issue_type}" + \
                    f"{title:{title_size}.{title_size}}{sep}"
            except IndexError:
                row += f"{' ' * icw}{sep}"
        rows.append(row)
    return rows


def get_header_row(columns, icw, separator):
    header_row = ''
    for column in columns:
        size = icw + len(BOLD) + len(END)
        bold_column = get_text_bold(column[:icw].upper())
        sep = separator if column != columns[-1] else ''
        header_row += f"{bold_column:^{size}.{size}}{sep}"
    return header_row


def main():
    columns = json.loads(os.getenv('LISTS'))
    issues = json.loads(os.getenv('ISSUES'))
    terminal_width = int(os.getenv('WIDTH'))

    issues.reverse()

    separator = ' | '
    separators_size = (len(columns) - 1) * len(separator)
    width_without_separators = terminal_width - separators_size
    # individual column width
    icw = math.floor(width_without_separators / len(columns))

    header_row = get_header_row(columns, icw, separator)
    rows = get_rows(issues, columns, icw, separator)

    print('‾' * terminal_width)
    print(header_row)
    print('_' * terminal_width)

    for row in rows:
        print(row)


if __name__ == '__main__':
    main()
