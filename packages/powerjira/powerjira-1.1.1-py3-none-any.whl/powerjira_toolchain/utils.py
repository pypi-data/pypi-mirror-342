from pathlib import Path, PurePosixPath
from rich import print
import subprocess
from sys import exit
from tabulate import tabulate
from typing import List, Dict
from jira import JIRA, Issue
from yaml import safe_load
import re
from dataclasses import dataclass
from datetime import datetime
from powerjira_toolchain.params import *

jira = JIRA(server=domain, basic_auth=(user_name, token))


def errorMessage(message:str) -> None:
  '''generic error messageing'''
  print(f'[red][bold]Error[/bold]. {message}[/red]')
  exit(1)


def verifyPath(path:str) -> None:
  '''check if input and output paths are valid, exits if not'''
  path_object = Path(path)
  format = PurePosixPath(path).suffix.lower()[1:]
  if not path_object.exists():
    errorMessage(f'Path {path} does not exist.')
    exit(1)
  elif not path_object.is_file():
    errorMessage(f'Path {path} is not a file.')
    exit(1)
  elif format not in ['yml', 'txt']:
    errorMessage(f'Input format "{format}" not supported, must be one of: yml, .txt')
    exit(1)


def readConfig(config_path:str) -> Dict[str,any]:
  '''reads config file and returns config as dict'''
  with open(config_path, 'r') as raw_config:
    return safe_load(raw_config)


def ensureTemplateTree(destination_path:str) -> None:
  """
  Ensures the existance of the following file tree, creating when needed:
    <powerjira_directory>/
      - ticket.yml
      - summary.txt
      - description.txt
  """
  destination = Path(destination_path).expanduser().resolve()
  destination.mkdir(parents=True, exist_ok=True)

  for filename,content in templates.items():
    dest_item = destination / filename
    if not dest_item.exists():
      with open(dest_item, 'w') as f:
        f.write(content)
        print(f"Created file {destination}/{filename}.")


def openPowerJiraDirectory(editor:str) -> None:
  '''opens powerjira directory in editor'''
  match editor:
    case 'vscode':
      subprocess.run(f'code -n {powerjira_directory}', shell=True, capture_output=True, text=True, executable=powerjira_shell)
    case _:
      errorMessage(f'Editor {editor} not supported.')


def formatTicketString(ticket:Issue, branch_name:str, parent_branch:str, style:str=result_table_style) -> str:
  '''builds string per ticket info to print'''
  #───GLANCE───────────────────
  if len(ticket.fields.summary) < ticket_excerpt_length:
    formatted_summary = ticket.fields.summary
  else:
    formatted_summary = ticket.fields.summary[:ticket_excerpt_length-3] + '...'
  if ticket.fields.description:
    if len(ticket.fields.description) < ticket_excerpt_length:
      formatted_description = ticket.fields.description
    else:
      formatted_description = ticket.fields.description[:ticket_excerpt_length-3] + '...'
  else:
    formatted_description = "(no description provided)"
  # TODO: images in description break things, handle that

  payload = '\n[bold green]GLANCE[/bold green]\n'
  payload += f'{ticket.fields.reporter} 👉 {ticket.fields.assignee}'
  payload += f'\n[bold italic]───Summary[/bold italic]\n{formatted_summary}'
  payload += f'\n[bold italic]───Description[/bold italic]\n{formatted_description}\n'

  #───TICKET───────────────────
  created_date_formatted = datetime.strptime(ticket.fields.created, "%Y-%m-%dT%H:%M:%S.%f%z").strftime('%Y-%m-%d %H:%M:%S')
  info_table = tabulate([
    ['Key', ticket.key],
    ['Url', f'{domain}/browse/{ticket.key}'],
    ['Type', ticket.fields.issuetype.name],
    ['Created', created_date_formatted],
    ['Status', ticket.fields.status.name],
    ['Priority', ticket.fields.priority.name if ticket.fields.priority else 'None']
  ], tablefmt=style)
  payload += f'\n[bold green]TICKET[/bold green]\n'
  payload += f'{info_table}\n'

  #───GLANCE───────────────────
  payload += f'\n[bold green]GIT COMMANDS[/bold green]\n'
  git_table = tabulate([
    ['Create Branch', f'git checkout -b {branch_name}'],
    ['GitLab MR', f'git push origin {branch_name} -o merge_request.create -o merge_request.target={parent_branch}'],
    ['GitHub PR', f"gh pr create --title 'TITLE' --body 'BODY' --base '{parent_branch}' --head '{branch_name}'"]
  ], tablefmt=style)
  payload += f'{git_table}\n'

  return payload


def buildTable(data:List[any], title:str, headers:List[str]=None, style:str=result_table_style) -> str:
  '''assembles table, with all the fixings'''
  table = tabulate(data, headers=headers, tablefmt=style)
  return f"\n[bold green]{title}[/bold green]\n{table}\n"


def getUserID(search_name:str, session_object=jira) -> str:
  '''Get USER ID
  fetches a user's user-id from jira, can be:
    - email (iyep@halcyon.ai)
    - email without domain (iyep)
    - full name (Isaac Yep)
    - first name and last initial (Isaac Y)
  '''
  user_search_result_list = session_object.search_users(query=search_name)
  if user_search_result_list:
    return user_search_result_list[0].accountId
  else:
    print(f"No users found by search term `{search_name}`")
    exit(1)


def substituteDynamicParams(input_string:str, params_dict:Dict[str, any]) -> str:
  """Substitute Dynamic Parameters
  Replaces substrings enclosed in angle brackets with corresponding values from a dictionary.

  Args:
    input_string (str): The input string containing substrings enclosed in angle brackets.
    params_dict (dict): A dictionary mapping parameter names to their replacement values.

  Returns:
    str: The input string with parameters substituted.
  """
  def replaceMatch(match):
    key = match.group(1)
    return params_dict.get(key, match.group(0))  # Replace if key exists, else keep original

  pattern = r"<(.*?)>"
  return re.sub(pattern, replaceMatch, input_string)


@dataclass
class regexCheck:
  """Regex checker match-case usage"""
  string: str
  def __eq__(self, other: str | re.Pattern):
    if isinstance(other, str):
      other = re.compile(other)
    assert isinstance(other, re.Pattern)
    return other.fullmatch(self.string) is not None
