# **powerjira**
*Get rid of the guff, because tickets should be simple.*

<br />

## **Welcome to powerjira!**
Put plainly, I don't enjoy my time in the Jira GUI. There's too much crap I don't care about, and even when you make your own ticket dashboard via JQL, the ticket views themselves could stand to be more minimal. \
And that's where *powerjira* comes in ☕🤏

Open a minimal set of configuration files, whose location you control (defaults to `$HOME`), and interface with Jira in your favorite editor. It also offers an ergonomic way to manage watched tickets, and allows you to query tickets on key or status without having to remember JQL (because who wants that).

If you want to make tickets without the guff, I'm a `pip install` away!

<br />

## **Get Started 🚀**
<hr>

Export the following environment variables powerjira expects to be available for authentication:
```sh
export JIRA_DOMAIN=https://acme.atlassian.net
export JIRA_USERNAME=dingus@acme.com
export JIRA_TOKEN=abc123
```

Then:
```sh
pip install powerjira
pip install --upgrade powerjira

python -m powerjira --help
python -m powerjira init # stubs config if missing, opens in editor
```

<br />

## **Usage ⚙**
<hr>

For convenience, set some macro in your shell like:
```sh
alias pj='python -m powerjira'
```

Now the terminal is your ticketing interface:
```st
pj goto # opens config in editor

pj fetch QA-123 # shows ticket
pj "to do" # shows all your tickets
pj make # reads specs from your config
pj watched prune # un-watches all your 'DONE' watched tickets
pj watched list
```

<br />

## **Technologies 🧰**
<hr>

  - [Tabulate](https://pypi.org/project/tabulate/)
  - [Typer](https://typer.tiangolo.com/)
  - [PyYAML](https://pypi.org/project/PyYAML/)
  - [jira](https://pypi.org/project/jira/)

<br />

## **Contribute 🤝**
<hr>

If you have thoughts on how to make the tool more pragmatic, submit a PR 😊 \
Also see [TODOD](TODO.md) for feature roadmap.

Documentation on the python jira module can be [explored here](https://jira.readthedocs.io/api.html#jira.client.JIRA).

<br />

## **License, Stats, Author 📜**
<hr>

<img align="right" alt="example image tag" src="https://i.imgur.com/ZHnNGeO.png" width="200" />

<!-- badge cluster -->
![PyPI - License](https://img.shields.io/pypi/l/powerjira?style=plastic)
![PyPI - Version](https://img.shields.io/pypi/v/powerjira)
![GitHub repo size](https://img.shields.io/github/repo-size/anthonybench/powerjira)
<!-- / -->

See [License](LICENSE) for the full license text.

This package was authored by *Isaac Yep*.