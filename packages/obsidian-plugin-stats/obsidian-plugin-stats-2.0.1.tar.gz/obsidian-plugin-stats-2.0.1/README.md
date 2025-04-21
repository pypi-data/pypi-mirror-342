# Obsidian Plugin Stats
Fetch and maintain [Obsidian](https://readwithai.substack.com/p/what-exactly-is-obsidian) plugin download stats from the command-line.

Obsidian provides quite detailed statistics about its plugins in JSON format at `https://raw.githubusercontent.com/obsidianmd/obsidian-releases/HEAD/community-plugin-stats.json` . These are easy to parse. I previously used the following script using [curl](https://www.man7.org/linux/man-pages/man1/curl.1.html) and [jq](https://github.com/jqlang/jq) to get statistics:
```
curl --silent https://raw.githubusercontent.com/obsidianmd/obsidian-releases/HEAD/community-plugin-stats.json | jq ".[\"${1:-plugin-repl}\"]"
```

One limitation is that these are statistics at a particular time. It would be nice to see these change over time so that I can have a feeling of progress.

For this reason, I made this tool which keeps track of statistics over time.

# Installation
You can install this tool with [pipx](https://github.com/pypa/pipx):

```
pipx install obsidian-plugin-stats
```


# Usage
The following shows the number of downloads for the plugin `plugin-repl`

```
obsidian-plugin-stats plugin-repl
```

Note that this will return the same value for the entire day (though these statistics appear to only be updated daily anyway).

You can raw statistics with `--raw` like so:

```
obsidian-plugin-stats --raw plugin-repl
```

You can get a timeseries of historic data in [the JSONL format](https://www.atatus.com/glossary/jsonl/) using
```
obsidian-plugin-stats --timeline plugin-repl
```

To maintain statistics you may wish to run obsidian-plugin-stats daily using, for example, a [systemd timer](https://www.freedesktop.org/software/systemd/man/latest/systemd.timer.html) or [cron job](https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/).

If this data is valuable to you might like to back up `~/.local/state/obsidian-plugin-stats`. I have this symlinked to a directory which I back up.

# Support
If you found this tool useful you could make a donation ($2 maybe?) [on my ko-fi](https://ko-fi.com/c/92004bdf98)  which will incentivize me to make and maintain tools like this.

Also, if you looked at this tool you are likely making a plugin for Obsidian. You may well be interested in my tool [Plugin REPL](https://readwithai.substack.com/p/obsidian-plugin-repl) which is designed to rapidly scripting Obsidian and iterating on plugins.

# About me
I am @readwithai I make tools related to reading and research sometimes using the [Obsidian markdown editor]. I get quite a lot of value from using Obsidian for "drive-by" note taking while coding, Obsidian makes it easy to quickly find a page and jot down some notes in a place where you will find it again when thinking about the same thing. I wrote some notes about this [here](https://readwithai.substack.com/p/drive-by-note-taking-in-obsidian) .

I also tend to produce a [stream of productivity tools](https://readwithai.substack.com/p/my-productivity-tools) like this.

If any of this sounds interesting you can follow me on [X](https://x.com/readwithai) where I write about this sort of thing.  If you are interested in Obsidian, note-taking or research you might like my [blog](https://readwithai.substack.com/).

![@readwithai logo](./logo.png)
