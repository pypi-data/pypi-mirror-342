# 🌀 bluer-options

🌀 `bluer_options` implements an `options` argument for Bash.

## installation

```bash
pip install bluer_options
```

add this line to your `~/.bash_profile` or `~/.bashrc`,

```bash
source $(python3 -m bluer_options locate)/.bash/bluer_options.sh
```

## usage

let your function receive an `options` argument, then parse it with `bluer_ai_option`, `bluer_ai_option_choice`, and `bluer_ai_option_int`.

```bash
function func() {
    local options=$1

    local var=$(bluer_ai_option "$options" var default)
    local choice=$(bluer_ai_option_choice "$options" value_1,value_2,value_3 default)
    local key=$(bluer_ai_option_int "$options" key 0)

    [[ "$key" == 1 ]] &&
        echo "choice=$choice,var=$var"
}
```

<details>
<summary>example 1</summary>

here is an example use of an `options` in the [vancouver-watching 🌈](https://github.com/kamangir/vancouver-watching) ingest command:


```bash
 > @help vanwatch ingest
```
```bash
vanwatch \
	ingest \
	[area=<area>,count=<-1>,~download,dryrun,~upload] \
	[-|<object-name>] \
	[process,count=<-1>,~download,dryrun,gif,model=<model-id>,publish,~upload] \
	[--detect_objects 0] \
	[--overwrite 1] \
	[--verbose 1]
```

this command takes in an `options`, an `object`, and `args`. an `options` is a string representation of a dictionary, such as,

```bash
area=<vancouver>,~batch,count=<-1>,dryrun,gif,model=<model-id>,~process,publish,~upload
```

which is equivalent, in json notation, to,

```json
{
    "area": "vancouver",
    "batch": false,
    "count": -1,
    "dryrun": true,
    "gif": true,
    "model": "<model-id>",
    "process": false,
    "publish": true,
    "upload": false,
}
```

for more refer to 🔻 [giza](https://github.com/kamangir/giza).

</details>

<details>
<summary>example 2</summary>

from [reddit](https://www.reddit.com/r/bash/comments/1duw6ac/how_can_i_automate_these_tree_commands_i/)

> How can I automate these tree commands I frequently need to type out?
I would like to run:
```bash
git add .
git commit -m "Initial "commit"
git push
```
> I got bored of typing them out each time. Can I make an alias or something like "gc" (for git commit). The commit message is always the same "Initial commit".

first, install `bluer-options`. this will also install [`blueness`](https://github.com/kamangir/blueness).

```bash
pip install bluer_options
```

then, copy [`example1.sh`](./bluer_options/assets/example1.sh) to your machine and add this line to the end of your `bash_profile`,

```bash
source <path/to/example1.sh>
```

now, you have access to the `@git` super command. here is how it works.

1. `@git help` shows usage instructions (see below).
1. `@git commit` runs the three commands. you can customize the message by running `@git commit <message>`. you can also avoid the push by running `@git commit <message> ~push`.
1. for any `<task>` other than `commit`, `@git <task> <args>` runs `git <task> <args>`.

```
 > @git help
 @git commit [<message>] \
	~push
 . git commit with <message> and push.
@git <command>
 . git <command>.
 ```

![image](https://raw.githubusercontent.com/kamangir/assets/main/blue-options/example1.png)

</details>

---

> 🌀 [`blue-options`](https://github.com/kamangir/blue-options) for the [Global South](https://github.com/kamangir/bluer-south).

---

[![pylint](https://github.com/kamangir/bluer-options/actions/workflows/pylint.yml/badge.svg)](https://github.com/kamangir/bluer-options/actions/workflows/pylint.yml) [![pytest](https://github.com/kamangir/bluer-options/actions/workflows/pytest.yml/badge.svg)](https://github.com/kamangir/bluer-options/actions/workflows/pytest.yml) [![PyPI version](https://img.shields.io/pypi/v/bluer-options.svg)](https://pypi.org/project/bluer-options/) [![PyPI - Downloads](https://img.shields.io/pypi/dd/bluer-options)](https://pypistats.org/packages/bluer-options)
