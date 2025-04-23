from rich import print
from rich.pretty import Pretty
from sys import exit
import typer
from jira import JIRAError
from powerjira_toolchain.params import *
from powerjira_toolchain.utils import *

app = typer.Typer(help="Jira Tickets without the guff")


@app.command()
def init():
  '''Creates the powerjira directory structure, or populates missing files. Opens in editor'''
  ensureTemplateTree(powerjira_directory)
  openPowerJiraDirectory(powerjira_editor)


@app.command()
def goto():
  '''Opens powerjira directory in edtitor'''
  openPowerJiraDirectory(powerjira_editor)


@app.command()
def make(dry_run:bool=False):
  '''Builds ticket per <powerjira_directory>/ticket.yml'''
  # file guards
  verifyPath(f'{powerjira_directory}/ticket.yml')
  verifyPath(f'{powerjira_directory}/summary.txt')
  verifyPath(f'{powerjira_directory}/description.txt')

  # read config
  config = readConfig(powerjira_directory + '/ticket.yml')
  try:
    reporter = config['reporter']
    assignee = config['assignee']
    init_status = config['init_status']
    project = config['project'].upper()
    priority = config['priority'].title()
    issue_type = config['issue_type'].title()
    parent_epic = config['parent_epic']
    parent_branch = config['parent_branch']
    branch_name_params = config['branch_name_params']
    branch_naming_convention = config['branch_naming_convention']
  except KeyError as ke:
    errorMessage(f'Missing config key: {ke}')

  # guard for <ticket_key> in branch_naming_convention
  if '<ticket_key>' not in branch_naming_convention:
    errorMessage('Branch naming convention must include <ticket_key>.')

  # build payload
  with open(f'{powerjira_directory}/summary.txt', 'r') as summary, open(f'{powerjira_directory}/description.txt', 'r') as description:
    summary = summary.read().rstrip('\n')
    description = description.read().rstrip('\n')
  ticket_blueprint = {
      'reporter': {'accountId': getUserID(reporter)},
      'assignee': {'accountId': getUserID(assignee)},
      'project': {'key': project},
      'issuetype': {'name': issue_type},
      'summary': summary,
      'description': description
    }
  if issue_type.lower() == 'task' :
    ticket_blueprint['priority'] = {'name': priority}
    if parent_epic:
      ticket_blueprint['parent'] = {'key': parent_epic}
  elif issue_type.lower() == 'epic' and parent_epic:
    errorMessage('Can not assign epic as child to another epic.')

  # make or dry-run
  if dry_run:
    print('ℹ️ Dry Run: Would have created:')
    print(Pretty(ticket_blueprint, expand_all=True))
    exit(0)
  else:
    new_issue = jira.create_issue(fields=ticket_blueprint)
    status_id = jira.find_transitionid_by_name(new_issue.key, init_status)
    jira.transition_issue(new_issue.key, transition=status_id)
    branch_name = substituteDynamicParams(branch_naming_convention.replace('<ticket_key>', new_issue.key), branch_name_params)
    print(formatTicketString(jira.issue(new_issue.key), branch_name=branch_name,  parent_branch=parent_branch))
    exit(0)


@app.command()
def fetch(target:str):
  '''Provide ticket key, or a status for all your related open tickets'''
  match regexCheck(target):
    case r"^.+-\d+$": # ticket key
      verifyPath(f'{powerjira_directory}/ticket.yml')
      config = readConfig(powerjira_directory + '/ticket.yml')
      try:
        parent_branch = config['parent_branch']
        branch_name_params = config['branch_name_params']
        branch_naming_convention = config['branch_naming_convention']
      except KeyError as ke:
        errorMessage(f'Missing config key: {ke}')
      try:
        issue = jira.issue(target)
        branch_name = substituteDynamicParams(branch_naming_convention.replace('<ticket_key>', issue.key), branch_name_params)
        print(formatTicketString(issue, branch_name=branch_name, parent_branch=parent_branch))
      except JIRAError as e:
        errorMessage(f'Ticket [bold]{target}[/bold] not found.')
      exit(0)

    case _: # assume status
      try:
        issues = jira.search_issues(f'status = "{target}" AND assignee = currentUser()')
        print(buildTable([[t.key, t.fields.summary] for t in issues], title=f"My '{target}'", headers=['Ticket Key', 'Summary (title)']))
      except JIRAError as e:
        errorMessage(f'Status [bold]{target}[/bold] not found.')
      exit(0)


@app.command()
def watched(action:str):
  '''[list, done] Manage watched issues of status DONE'''
  watched_issues = jira.search_issues('watcher = currentUser() AND resolution = Done')

  title = {
    'prune': 'Un-Followed Issues',
    'list': 'Watched Issues'
  }[action]
  payload = []
  
  for issue in watched_issues:
    match action:
      case 'prune':
        resolution = str(issue.fields.resolution)
        if resolution.lower() == 'done':
          jira.remove_watcher(issue.key, user_name)
          payload.append([issue.key, issue.fields.summary])
      case 'list':
        payload.append([issue.key, issue.fields.summary])

  print(buildTable(payload, title=title, headers=['Ticket Key', 'Summary (title)']))
  exit(0)
