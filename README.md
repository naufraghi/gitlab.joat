# Gitlab CLI

Config files for a joat based cli, you don't know what is joat? 😱
get your shit together and go [read about joat!](https://github.com/sennav/joat)

For now this cli is focused in managing tickets, but nothing stops it to expand to other gilab APIs.
It's also very specific to my needs so let me know if you are using this so I can make it more generic.

## Instalation

In a near future:

```
joat install sennav/gitlab
```

For now just clone this repo in your home folder with under the folder `.gitlab.joat` and create a symlink in your path name `gitlab` pointing to your `joat` binary.

## Usage

It's used like a regular CLI, here's the help with the commands:

```
gitlab-cli 0.0.1 (joat 0.0.2)
Vinicius <senna.vmd@gmail.com>
Cli to interface with Gitlab's REST API

USAGE:
    gitlab [FLAGS] [OPTIONS] [SUBCOMMAND]

FLAGS:
    -h, --help       Prints help information
    -V, --version    Prints version information
    -v               Sets the level of verbosity

OPTIONS:
    -c, --config <FILE>    Sets a custom config file

SUBCOMMANDS:
    add_milestone        Add issue to milestone
    auto_complete        Create auto complete script
    board                Print board
    boards               List boards
    cleanlabels          Return the issue's list of labels without workflow labels
    code                 Move issue to code in progress column
    done                 Move ticket to done column
    edit                 Edit an issue
    help                 Prints this message or the help of the given subcommand(s)
    issues               List issues
    milestone            List milestone tickets by the milestone name (substring)
    milestone_by_name    Return milestone id by a substring name
    milestones           Get project milestones
    new                  Create an issue in the ready for dev column
    newissue             Create an issue
    project              Show project data
    project_users        Show project users
    show                 Show issue data

```

## Config

You need to set the following environment variables:
* `GITLAB_TOKEN` - your gitlab token, google how to get one :)
* `GITLAB_PROJECT_ID` - the project id you want to work on.
