# arxiv-visual-summary

Tool for extracting a visual summary of new papers uploaded to ArXiv.

To setup:

```
$ git clone https://github.com/kylemcdonald/arxiv-visual-summary.git
$ cd arxiv-visual-summary
$ pip install -U -r requirements.txt
```

Then to update the files, run:

```
$ python update.py
```

This will take a long time the first time, because it's downloading a lot of papers and running ImageMagick using `convert`.

`update.py` should be run once a day, and it will save a `.pkl` file to keep track of when the RSS changes.

Finally, you need to host this directory from a webserver. I run this in the public directory on a node.js express server, but it should run anywhere that can host static files.
