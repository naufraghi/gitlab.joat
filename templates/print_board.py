#!/usr/bin/python

import os
import re
import math

END = '\033[0m'
BOLD = '\033[1m'
RED = '\033[91m'
BLUE = '\033[36m'


def write_red(text):
    return '{}{}{}'.format(RED, text, END)


def write_bold(text):
    return '{}{}{}'.format(BOLD, text, END)


def get_initials(assignee):
    try:
        names = assignee.upper().split('.')
        if len(names) > 1:
            initials = names[0][0] + names[1][0]
            return initials
        return names[0][0] + names[0][1]
    except Exception as e:
        return '  '


def get_ticket_number(raw_line):
    ticket_number = re.search('^<:id>≤≤([^≥]*)≥≥', raw_line).group(1)
    if len(ticket_number) < 5:
        no_spaces = 5 - len(ticket_number) + 1
        ticket_number = ticket_number + (' ' * no_spaces)
    return ticket_number


def get_ticket_type(raw_line):
    ticket_type = re.search('<:labels>≤≤([^≥]*)≥≥', raw_line).group(1)

    if 'Feature' in ticket_type:
        return '🚀'
    if ticket_type == 'Bug':
        return '🐛'
    if ticket_type == 'Tech improvement':
        return '🤖'
    if ticket_type == 'Requirement work':
        return '📝'
    if ticket_type == 'Improvement':
        return '🎨'
    if ticket_type == 'Tech support task':
        return '🔧'
    if ticket_type == 'Sub-task':
        return '🍕'
    return '🤔'


def get_assignee(raw_line):
    assignee = re.search('<:assignee>≤≤([^≥]*)≥≥', raw_line).group(1)
    if assignee == 'unassigned':
        return '    '
    initials = '({})'.format(get_initials(assignee))
    return initials


def get_description(raw_line):
    return re.search('<:title>≤≤([^≥]*)≥≥', raw_line).group(1)


def get_line(from_list, line_no, icw):
    try:
        raw_line = from_list[line_no]
        if raw_line == '':
            return ' ' * icw
        ticket_number = get_ticket_number(raw_line)
        ticket_type = get_ticket_type(raw_line)
        assignee = get_assignee(raw_line)
        description = get_description(raw_line)
        description_size = icw - 6 - 5 - 3  # Ticket number 6 char, assignee 4 + 1 space, 2 + 1 space  ticket type
        if description_size <= 0:
            return 'Terminal too small!!!'
        output = '{ticket_number}{ticket_type} {assignee} {description:{w}.{w}}'.format(
                ticket_type=ticket_type,
                ticket_number=write_bold(ticket_number),
                assignee=write_red(assignee),
                description=description,
                w=description_size)
        return output
    except IndexError:
        return ' ' * icw


def print_headers(icw, separator, total_width):
    print(
        '{ready_for_dev:^{w}.{w}}{separator}'
        '{coding:^{w}.{w}}'
        .format(
            ready_for_dev=write_bold('Ready for dev'),
            coding=write_bold('In progress'),
            separator=separator,
            w=(icw + len(BOLD) + len(END))
        ))
    print('-' * total_width)


def main():
    ready_for_dev = os.getenv('READY').split('\n')
    progress = os.getenv('PROGRESS').split('\n')
    ready_for_dev.reverse()
    progress.reverse()

    no_rows = max(
        len(ready_for_dev),
        len(progress),
    )

    terminal_width = int(os.getenv('WIDTH'))
    separator = ' | '
    width_without_separators = terminal_width - 1 * len(separator)
    icw = math.floor(width_without_separators / 2)  # individual column width

    print_headers(icw, separator, terminal_width)
    for i in range(0, no_rows):
        print(
            '{ready_for_dev}{separator}'
            '{coding}'.format(
                ready_for_dev=get_line(ready_for_dev, i, icw),
                coding=get_line(progress, i, icw),
                separator=separator,
            ))


if __name__ == '__main__':
    main()
