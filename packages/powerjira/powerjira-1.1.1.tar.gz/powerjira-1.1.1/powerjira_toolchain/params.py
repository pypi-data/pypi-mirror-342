from os import getenv

user_name = getenv('JIRA_USERNAME')
token = getenv('JIRA_TOKEN')
domain = getenv('JIRA_DOMAIN')
home_dir = getenv('HOME')

ticket_excerpt_length = 60
default_powerjira_directory = f'{home_dir}/powerjira'
default_shell = '/bin/zsh'
default_editor = 'vscode'
default_powerjira_table_style = 'rounded_outline'

templates = {
  'ticket.yml': '''# pj --help

#───TICKET───────────────────
reporter: jack
assignee: jill

init_status: to do # new, to do, in progress, done, backlog

project: sales # sales, marketing, frontend
priority: medium # low, medium, high (ignored if epic)
issue_type: task # task, epic
parent_epic: '' # leave empty for standalone task or epic


#───GIT──────────────────────
parent_branch: main
# ℹ️ naming convention must include <ticket_key>
branch_naming_convention: feature/<ticket_key>_<branch_suffix>
branch_name_params: # custom branch name parameters
  branch_suffix: implement_thing''',

  'summary.txt': '''This is the ticket's title, which jira calls the "summary"''',

  'description.txt': '''This is the ticket's description''',
}

#TODO: implement override in sleepyconfig.yml
result_table_style = default_powerjira_table_style if True else ''
powerjira_directory = default_powerjira_directory if True else ''
powerjira_shell = default_shell if True else ''
powerjira_editor = default_editor if True else ''