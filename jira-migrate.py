#!/usr/bin/env python

import argparse

import requests


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'gitlab_user',
        help='Must be administrator.')
    parser.add_argument(
        'gitlab_token',
        help="Can be generated under 'Settings->Access Tokens' in Gitlab")
    parser.add_argument(
        'gitlab_url',
        help="Url of Gitlab instance without ending '/'")
    parser.add_argument(
        'jira_user',
        help='User to connect to JIRA, see https://docs.gitlab.com/ee/user/project/integrations/jira.html')  # noqa E501
    parser.add_argument(
        'jira_password',
        help='Password to connect to JIRA, see https://docs.gitlab.com/ee/user/project/integrations/jira.html')   # noqa E501
    parser.add_argument(
        'jira_url',
        help="Url of the JIRA instance")
    parser.add_argument(
        '--dry-run',
        action='store_true', help="Do not actually change anything.")
    args = parser.parse_args()

    # Get all projects
    page = '0'
    projects = []
    while True:
        r = requests.get(
            args.gitlab_url + '/api/v4/projects',
            headers={
                'Sudo': args.gitlab_user,
                'Private-Token': args.gitlab_token,
            },
            params={
                'page': page,
                'per_page': 100,  # maximum
            },
        )
        r.raise_for_status()  # Hard fail on failure
        projects = projects + r.json()
        page = r.headers.get('X-Next-Page')
        if not page:
            break

    # Change JIRA for all projects
    for p in projects:
        id = p['id']
        name = p['name_with_namespace']
        print("Edit id: {}, name: {}".format(id, name))

        # Do not change anything on dry-run
        if args.dry_run:
            continue

        # Put new JIRA config
        r = requests.put(
            args.gitlab_url + '/api/v4/projects/{}/services/jira'.format(id),
            headers={
                'Sudo': args.gitlab_user,
                'Private-Token': args.gitlab_token,
            },
            json={
                'url': args.jira_url,
                'username': args.jira_user,
                'password': args.jira_password,
            }
        )
        r.raise_for_status()  # Hard fail on failure


if __name__ == "__main__":
    main()
