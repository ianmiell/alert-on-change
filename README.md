# alert-on-change

## tl;dr

Make a PR on [requests.txt](https://github.com/ianmiell/alert-on-change/blob/master/requests.txt) like this:

```
+curl somewebsite.com	you@example.com
```

and this will automatically mail you when the output of the command changes.


This sends an email when the output of a command changes. For example:

```
curl somewebsite.com 
```

or even:

```
curl somewebsite.com | html2text | grep -wi shutit | wc -l
```

Obviously, the output of this can change a little bit, so you can specify a percentage of words common to old and new in the output and it will work out if the diff has less than that percentage of words in common. This defaults to 100, so any change will mail you.

## Adding Your Command

I accept pull requests for new commands and mail addresses.

Make a PR on requests.txt, the format is:

```
+<COMMAND><TAB><EMAIL ADDRESS><TAB><PERCENT COMMON THRESHOLD>
``

eg

```
+curl bbc.co.uk/news	test@test.com	80
```

Your request, if and when accepted, will get an id (which you will see in DATA.sql). If you want one removed, do the same, but with a '-' at the start, eg:

```
-curl bbc.co.uk/news	test@test.com	80
```

## How Does it Work?

Internally, it uses 'dwdiff -s' to gather stats on the difference between the output when the last mail was sent and the current one.

All the code and data is stored on github, and the application is phoenix-deployed using [ShutIt](https://github.com/ianmiell/shutit.git)
