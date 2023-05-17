import pathlib
import typing
from typing import Any
import sklearn
import numpy as np
from config import Config
from repohandle import HandleRepo

class Setup(HandleRepo):
	def __init__(self) -> None:
		super().__init__()
		self.config = Config()
	
	def prep_dir(self, dir) ->  typing.List:
		return sorted([file for file in dir.iterdir() if file.suffix == ".pkl"])

	def retrieve_data_object(self, path) -> np.ndarray:
		ab_dataset = self.prep_dir(path)
		out = {}  
		for idx,file_pth in enumerate(ab_dataset):
			temp = self.unpickle(file_pth)
			out["CCS-" + str(idx)]  = temp
		return out
	
	def retrieve_targets(self) -> np.ndarray:
		return self.retrieve_data_object(self.config.tgt_pth)
	
	def retrieve_nsr_features(self) -> np.ndarray:
		return self.retrieve_data_object(self.config.dsr_pth)

	def retrieve_dsr_features(self):
		return self.retrieve_data_object()

	def _regression_models(self):
		return {
			sklearn.svm.SVR().__class__.__name__ : sklearn.svm.SVR(),
			sklearn.linear_model.BayesianRidge().__class__.__name__ : sklearn.linear_model.BayesianRidge(),
			sklearn.neural_network.MLPRegressor().__class__.__name__ : sklearn.neural_network.MLPRegressor(),
			sklearn.neighbors.KNeighborsRegressor().__class__.__name__ : sklearn.neighbors.KNeighborsRegressor(),
			sklearn.ensemble.RandomForestRegressor().__class__.__name__ : sklearn.ensemble.RandomForestRegressor()
		}

	def _metrics(self, actual, pred):
		metrics = sklearn.metrics
		return {
			metrics.mean_squared_error.__name__ : metrics.mean_squared_error(actual, pred),
			metrics.mean_absolute_error.__name__ : metrics.mean_absolute_error(actual, pred),
			metrics.mean_squared_log_error.__name__ : metrics.mean_squared_log_error(actual, pred),
			"root_" + metrics.mean_squared_error.__name__ : np.sqrt(metrics.mean_squared_error(actual, pred))
		}

class ABResults(Setup):
	def __init__(self) -> None:
		super().__init__()
	
	def nsr_exp(self):
		pass

	def dsr_exp(self):
		pass

	def throughput(self):
		pass

class DSResults(Setup): 
	def __init__(self) -> None:
		super().__init__()

	def nsr_exp(self):
		pass
	
	def dsr_exp(self):
		pass

	def throughput(self):
		pass

class CompSOA(Setup):
	def __init__(self) -> None:
		super().__init__()
	
	def nsr_exp(self):
		pass
	
	def dsr_exp(self):
		pass

	def throughput(self):
		pass
