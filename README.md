# Cycling GC Tracker

This projects plots the gaps among the riders in the General classification during a Grand Tour to
give a visual representation of where each rider won or lost time.

To access the website, click [here](https://lauromoura.github.io/cyclinggctracker)

## How does it work?

To generate the static data, we scrape the ProCyclingStats (being easy on the bandwidth...) using
[BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) and create a json file with all
needed results. This json is then served through github.io and processed on the user browser
and drawn with [Flot](http://www.flotcharts.org/) in Javascript.

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/ee142cf9d53a4382b7c6d57f035559da)](https://www.codacy.com/app/lauromoura/cyclinggctracker?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=lauromoura/cyclinggctracker&amp;utm_campaign=Badge_Grade)
