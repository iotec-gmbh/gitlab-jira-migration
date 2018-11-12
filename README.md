# gitlab-jira-migration

If you are using [JIRA](https://de.atlassian.com/software/jira) and [Gitlab](https://about.gitlab.com/) and you would like to change the url, user or password of your JIRA instance, you can not simply change the template and all the JIRA integration of all projects are changes (see [issue](https://gitlab.com/gitlab-org/gitlab-ce/issues/25541)).
So you have to change every single project which is pretty annoying. 

Or you can use this script.

## Dependencies

This script is only tested with Python 3, but should also work with Python 2.

You need [Requests](http://docs.python-requests.org/en/master/) for HTTP calls.

## Usage

```
./jira-migrate.py --help
usage: jira-migrate.py [-h] [--dry-run]
                       gitlab_user gitlab_token gitlab_url jira_user
                       jira_password jira_url

positional arguments:
  gitlab_user    Must be administrator.
  gitlab_token   Can be generated under 'Settings->Access Tokens' in Gitlab
  gitlab_url     Url of Gitlab instance without ending '/'
  jira_user      User to connect to JIRA, see https://docs.gitlab.com/ee/user/
                 project/integrations/jira.html
  jira_password  Password to connect to JIRA, see https://docs.gitlab.com/ee/u
                 ser/project/integrations/jira.html
  jira_url       Url of the JIRA instance

optional arguments:
  -h, --help     show this help message and exit
  --dry-run      Do not actually change anything.
```

So e.g.

```
./jira-migrate.py max.mustermann secret-token https://gitlab.company.de gitlab gitlab-password https://company.atlassian.net
```
