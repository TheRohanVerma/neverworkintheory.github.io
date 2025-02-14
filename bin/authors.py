#!/usr/bin/env python

import argparse
import re
import sys

import util


SPECIAL = {
    'K. El Emam': 'El Emam, K.',
    'Guilherme Renna Rodrigues': 'Renna Rodrigues, Guilherme',
    'Mel Ó Cinnéide': 'Ó Cinnéide, Mel',
    'Santiago Perez De Rosso': 'Perez De Rosso, Santiago',
    'Arie van Deursen': 'van Deursen, Arie'
}

SPLIT = re.compile(r'\band\b')


def main():
    options = get_options()
    unreviewed = util.get_unreviewed(options.unreviewed)
    entries = util.get_entries(options.strings, options.input)
    entries = [e for e in entries if e['ID'] not in unreviewed]
    credit = {}
    for entry in entries:
        add_credit(credit, entry)
    report(credit)


def add_credit(credit, entry):
    eid = entry['ID']
    assert ('author' in entry) or ('editor' in entry), \
        f'No author or editor in {entry}'
    assert 'reviewed' in entry, \
        f'No review listed in {entry}'
    reviewed = entry['reviewed']
    source = entry['author'] if ('author' in entry) else entry['editor']
    for person in [x.strip() for x in SPLIT.split(source)]:
        person = util.unlatex(person)
        person = normalize(person)
        if person not in credit:
            credit[person] = []
        credit[person].append((eid, reviewed))


def get_options():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', help='specify input file')
    parser.add_argument('--strings', help='string definitions file')
    parser.add_argument('--unreviewed', help='text file with one key per line indicating unreviewed entries')
    return parser.parse_args()


def report(credit):
    print('<table>')
    print('<tr><th>Name</th><th>Citation</th><th>Reviewed</th></tr>')
    for person in sorted(credit.keys()):
        for (i, (key, reviewed)) in enumerate(credit[person]):
            p_col = f'<td>{person}</td>' if (i == 0) else '<td></td>'
            k_col = f'<td><a href="/bib/#{key}">{key}</a></td>'
            _, year, month, day, _ = reviewed.split('/')
            r_col = f'<td><a href="{{{{\'{reviewed}\' | relative_url}}}}">{year}-{month}-{day}</a></td>'
            print(f'<tr>{p_col}{k_col}{r_col}</tr>')
    print('</table>')


def normalize(person):
    if person in SPECIAL:
        return SPECIAL[person]
    front, back = person.rsplit(' ', 1)
    return f'{back}, {front}'

        
if __name__ == '__main__':
    main()
