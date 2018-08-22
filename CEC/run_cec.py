# encoding=utf8
import sys

import random
import logging
from numpy import asarray, savetxt
from NiaPy import Runner
from NiaPy.util import Task, TaskConvPrint, TaskConvPlot, OptimizationType
from cecargparser import getDictArgs, cdims

logging.basicConfig()
logger = logging.getLogger('cec_run')
logger.setLevel('INFO')

# For reproducive results
random.seed(1234)

class MinMB(object):
	def __init__(self, run_fun, Lower=-100, Upper=100, fnum=1):
		self.Lower, self.Upper = Lower, Upper
		self.fnum = fnum
		self.run_fun = run_fun

	def function(self):
		def evaluate(D, sol): return self.run_fun(asarray(sol), self.fnum)
		return evaluate

class MaxMB(MinMB):
	def function(self):
		f = MinMB.function(self)
		def e(D, sol): return -f(D, sol)
		return e

def getCecBench(cec, d):
	if cec == 5:
		sys.path.append('cec2005')
		from cec2005 import run_fun
		if d not in dims: raise Exception('Dimension sould be in %s' % (dims))
	elif cec == 8:
		sys.path.append('cec2008')
		from cec2008 import run_fun
	elif cec == 13:
		sys.path.append('cec2013')
		from cec2013 import run_fun
		if d not in dims: raise Exception('Dimension sould be in %s' % (dims))
	elif cec == 14:
		sys.path.append('cec2014')
		from cec2014 import run_fun
		if d not in dims: raise Exception('Dimension sould be in %s' % (dims))
	elif cec == 15:
		sys.path.append('cec2015')
		from cec2015 import run_fun
		if d not in dims: raise Exception('Dimension sould be in %s' % (dims))
	elif cec == 17:
		sys.path.append('cec2017')
		from cec2017 import run_fun
		if d not in dims: raise Exception('Dimension sould be in %s' % (dims))
	elif cec == 18:
		sys.path.append('cec2018')
		from cec2018 import run_fun
		if d not in dims: raise Exception('Dimension sould be in %s' % (dims))
	return run_fun

def getMaxFES(cec):
	if cec == 8: return 5000
	if cec in [5, 13, 14, 15, 17, 18]: return 10000

def simple_example(alg, cec, fnum=1, runs=10, D=10, nFES=50000, nGEN=5000, seed=None, optType=OptimizationType.MINIMIZATION, optFunc=MinMB, wout=False, sr=[-100, 100], **kwu):
	bests, func = list(), getCecBench(cec)
	for i in range(runs):
		task = Task(D=D, nFES=nFES, nGEN=nGEN, optType=optType, benchmark=optFunc(func, sr[0], sr[1], fnum))
		algo = alg(seed=seed, task=task)
		best = algo.run()
		logger.info('%s %s' % (best[0], best[1]))
		bests.append(best)
	if wout:
		bpos, bval = asarray([x[0] for x in bests]), asarray([x[1] for x in bests])
		savetxt('%s_%d_%d_p' % (algo.sName, fnum, D), bpos)
		savetxt('%s_%d_%d_v' % (algo.sName, fnum, D), bval)

def logging_example(alg, cec, fnum=1, D=10, nFES=50000, nGEN=5000, seed=None, optType=OptimizationType.MINIMIZATION, optFunc=MinMB, wout=False, sr=[-100, 100], **kwu):
	func = getCecBench(cec)
	task = TaskConvPrint(D=D, nFES=nFES, nGEN=nGEN, optType=optType, benchmark=optFunc(func, sr[0], sr[1], fnum))
	algo = alg(seed=seed, task=task)
	best = algo.run()
	logger.info('%s %s' % (best[0], best[1]))

def plot_example(alg, cec, fnum=1, D=10, nFES=50000, nGEN=5000, seed=None, optType=OptimizationType.MINIMIZATION, optFunc=MinMB, wout=False, sr=[-100, 100], **kwu):
	func = getCecBench(cec)
	task = TaskConvPlot(D=D, nFES=nFES, nGEN=nGEN, optType=optType, benchmark=optFunc(func, sr[0], sr[1], fnum))
	algo = alg(seed=seed, task=task)
	best = algo.run()
	logger.info('%s %s' % (best[0], best[1]))
	input('Press [enter] to continue')

def getOptType(otype):
	if otype == OptimizationType.MINIMIZATION: return MinMB
	elif otype == OptimizationType.MAXIMIZATION: return MaxMB
	else: return None

if __name__ == '__main__':
	pargs = getDictArgs(sys.argv[1:])
	pargs['nFES'] = round(pargs['D'] * getMaxFES(pargs['cec']) * pargs['reduc'])
	algo = Runner.getAlgorithm(pargs['algo'])
	optFunc = getOptType(pargs['optType'])
	if not pargs['runType']: simple_example(algo, optFunc=optFunc, **pargs)
	elif pargs['runType'] == 'log': logging_example(algo, optFunc=optFunc, **pargs)
	elif pargs['runType'] == 'plot': plot_example(algo, optFunc=optFunc, **pargs)
	else: simple_example(algo, optFunc=optFunc, **pargs)

# vim: tabstop=3 noexpandtab shiftwidth=3 softtabstop=3
