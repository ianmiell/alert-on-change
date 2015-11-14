# alert-on-change

## tl;dr

Make a PR on [requests.txt](https://github.com/ianmiell/alert-on-change/blob/master/requests.txt) like this:

```
+curl somewebsite.com	you@example.com	100	Track somewebsite.com
```

and this will automatically mail you when the output of the command changes. Note that fields are tab-delimited.

## Overview

This sends an email when the output of a command changes. For example:

```
curl somewebsite.com 
```

or even:

```
curl somewebsite.com | html2text | grep -wi shutit | wc -l
```

### Tuning the "Common Words Percentage Trigger"

Obviously, the output of this can change a little bit and you don't care (eg a timestamp on the page), so you can specify a percentage of words common to the old output and the new output and it will work out if the diff has less than that percentage of words in common before alerting you.

This defaults to 100, so any change will mail you. 0 would never mail you.

## Adding Your Command

I accept pull requests for new commands and mail addresses.

Make a PR on requests.txt, the format is:

```
+<COMMAND><TAB><EMAIL ADDRESS><TAB><PERCENT OF WORDS COMMON THRESHOLD><TAB><DESCRIPTION>
```

eg

```
+curl bbc.co.uk/news	test@test.com	80	BBC news check
```

Your request, if and when accepted, will get an id (which you will see in [DATA.sql](https://github.com/ianmiell/alert-on-change/blob/master/context/DATA.sql)). If you want one removed, do the same, but with a '-' at the start, eg:

```
-curl bbc.co.uk/news	test@test.com	80	BBC news check
```

## Why?

I often want to be alerted when a new version of software comes out and release notes updated, or when something is mentioned on a page.

Most services that provide this either require payment or are based on visual diffs. I only care about content, and don't want to pay.

## How Does it Work?

Internally, it uses 'dwdiff -s' to gather stats on the difference between the output when the last mail was sent and the current one.

All the code and data is stored on github, and the application is phoenix-deployed using a [ShutIt](https://github.com/ianmiell/shutit.git) [script](https://github.com/ianmiell/alert-on-change/blob/master/alert_on_change.py#L75)
