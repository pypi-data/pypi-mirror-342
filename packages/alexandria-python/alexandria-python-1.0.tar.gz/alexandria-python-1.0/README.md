# Alexandria

**Alexandria** is a Python package for Bayesian time-series econometrics applications. This is the first official release of the software. For its first release, Alexandria includes only the most basic model: the linear regression. However, it proposes a wide range of Bayesian linear regressions:

- maximum likelihood / OLS regression (non-Bayesian)
- simple Bayesian regression
- hierarchical (natural conjugate) Bayesian regression
- independent Bayesian regression with Gibbs sampling
- heteroscedastic Bayesian regression
- autocorrelated Bayesian regression

Alexandria is user-friendly and can be used from a simple Graphical User Inteface (GUI). More experienced users can also run the models directly from the Python console by using the model classes and methods.

===============================

**Installing Alexandria**

Alexandria can be installed from pip: 

	pip install alexandria-python

A local installation can also obtain by copy-pasting the folder containing the toolbox programmes. The folder can be downloaded from the project website or Github repo:  
https://alexandria-toolbox.github.io  
https://github.com/alexandria-toolbox  

===============================

**Getting started**

Simple Python example:

	# imports
	from alexandria import NormalWishartBayesianVar
	from alexandria import DataSets
	from alexandria import Graphics
	import numpy as np

	# load ISLM dataset
	ds = DataSets()
	islm_data = ds.load_islm()[:,:4]

	# create and train Bayesian VAR with default settings
	var = NormalWishartBayesianVar(endogenous = islm_data)
	var.estimate()

	# estimate forecasts for the next 4 periods, 60% credibility level
	forecast_estimates = var.forecast(4, 0.6)

	# create graphics of predictions
	gp = Graphics(var)
	gp.forecast_graphics(show=True, save=False)

===============================

**Documentation**

Complete manuals and user guides can be found on the project website and Github repo:  
https://alexandria-toolbox.github.io  
https://github.com/alexandria-toolbox  

===============================

**Contact**

alexandria.toolbox@gmail.com
