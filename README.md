# Street Tree Homology
Analysing the persistent homology of street tree locations in NYC and SF

See [the report](AJackson_StreetTreeHomology.pdf) for a summary.

We examine the persistent homology of street tree location samples in NYC and SF, hypothesising that the 
regular local level structure of NYC will cause statistically significant differents to the persistent 
homology of the SF samples.

Dependencies: [NumPy](http://www.numpy.org/), [MatPlotLib](https://matplotlib.org/), 
[Dionysus](http://mrzv.org/software/dionysus2/), [Diode](https://github.com/mrzv/diode).

[One file](visualise_street_trees.py) requires [HoloViews](http://holoviews.org/).

Much of the code is based on Katherine Turner's examples, and the rank function calculation on code 
provided by Vanessa Robins.

Recently added: a [Rips complex visualisation tool](rips_complex_visualisation.py).
Once run, you can click to add points then use a slider to adjust the radius for the complex, and view the 2-skeleton of the complex that results.
Dependencies: NumPy and MatPlotLib.
