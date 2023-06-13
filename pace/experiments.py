import typing
import argparse
import numpy as np
from config import Config
from repohandle import HandleRepo
from sklearn import metrics, svm, linear_model, neural_network, neighbors, ensemble

parser = argparse.ArgumentParser(description = "Research Question 1 Results")
parser.add_argument("-c", "--commit",  type = int, metavar = "", required = True, help = "Enter commit, (5: ABD, 50: DSD)")
parser.add_argument("-t", "--task",  type = str, metavar = "", required = True, help = "Enter task, (SR: Statistic Rep, DR: Neural Rep")
args = parser.parse_args()

class Setup(HandleRepo):
	def __init__(self) -> None:
		super().__init__()
		self.config = Config()
	
	def prep_dir(self, ids, dir) ->  typing.Tuple:
		return (
			sorted([i + 1 for i in range(ids)], reverse = True),
			sorted([file for file in dir.iterdir() if file.suffix == ".pkl"], reverse = True)
			)

	def retrieve_data_object(self, ids, dir) -> np.ndarray:
		ids, abds = self.prep_dir(ids, dir)
		out = {}  
		for id, abd in zip(ids, abds):
			temp = self.unpickle(abd)
			out[id]  = temp
		return out
	
	def _predictors(self):
		return [
			svm.SVR(), linear_model.BayesianRidge(), neural_network.MLPRegressor(),
			neighbors.KNeighborsRegressor(), ensemble.RandomForestRegressor()
		]

class RQ1(Setup):
	def __init__(self) -> None:
		super().__init__()
	
	def _get_data(self) -> typing.Tuple:
		return (
			self.retrieve_data_object(self.config.ABD_n, self.config.tgt_pth),
			self.retrieve_data_object(self.config.ABD_n, self.config.AB_sr_pth),
			self.retrieve_data_object(self.config.ABD_n, self.config.AB_nr_pth),
			self.retrieve_data_object(self.config.DSD_n, self.config.tgt_ds_pth),
			self.retrieve_data_object(self.config.DSD_n, self.config.DS_sr_pth),
			self.retrieve_data_object(self.config.DSD_n, self.config.DS_nr_pth)
	  )
	
	def _metrics(self, actual, pred) -> typing.Tuple:
		rmse = np.sqrt(metrics.mean_squared_error(actual, pred))
		mse = metrics.mean_squared_error(actual, pred)
		mae = metrics.mean_absolute_error(actual, pred)
		rmsle = metrics.mean_squared_log_error(actual, pred)
		avg = np.mean([rmse, mse, mae, rmsle])
		return rmse, mse, mae, rmsle, avg

	def _get_features(self, n, task):
		if n == 5 and task == "sr":
			ys, Xs, _, _, _, _ = self._get_data()
		elif n == 5 and task == "nr":
			ys, _, Xs, _, _, _ = self._get_data()
		elif n == 50 and task == "sr":
			_, _, _, ys, Xs, _ = self._get_data()
		elif n == 50 and task == "nr":
			_, _, _, ys, _, Xs = self._get_data()
		return Xs, ys
	
	def _predict(self, n, task):
		Xs, ys = self._get_features(n, task)
		predictor = neighbors.KNeighborsRegressor()
		out = []
		for _ in range(n):
			predictor.fit(Xs[n], ys[n])
			out.append(self._metrics(ys[n - 1], predictor.predict(Xs[n - 1])))
			n = n - 1
			if n == 1:
				break
		return out

print(RQ1()._predict(args.commit, args.task.lower()))


class RQ2(Setup): 
	def __init__(self) -> None:
		super().__init__()

class RQ3(Setup):
	def __init__(self) -> None:
		super().__init__()
	
	def nsr_exp(self):
		pass
	
	def dsr_exp(self):
		pass

	def throughput(self):
		pass
