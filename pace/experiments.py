import pathlib
import typing
# import sklearn
from sklearn import metrics, svm, linear_model, neural_network, neighbors, ensemble
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
	
	def retrieve_sr_features(self) -> np.ndarray:
		return self.retrieve_data_object(self.config.dsr_pth)

	def retrieve_dsr_features(self):
		return self.retrieve_data_object()

	def _predictors(self):
		return {
			svm.SVR().__class__.__name__ : svm.SVR(),
			linear_model.BayesianRidge().__class__.__name__ : linear_model.BayesianRidge(),
			neural_network.MLPRegressor().__class__.__name__ : neural_network.MLPRegressor(),
			neighbors.KNeighborsRegressor().__class__.__name__ : neighbors.KNeighborsRegressor(),
			ensemble.RandomForestRegressor().__class__.__name__ : ensemble.RandomForestRegressor()
		}
	
	def _fit(self, x, y):
		return [self._predictors()[predictor].fit(x, y) for predictor in self._predictors()]

	def _metrics(self, actual, pred):
		return {
			metrics.mean_squared_error.__name__ : metrics.mean_squared_error(actual, pred),
			metrics.mean_absolute_error.__name__ : metrics.mean_absolute_error(actual, pred),
			metrics.mean_squared_log_error.__name__ : metrics.mean_squared_log_error(actual, pred),
			"root_" + metrics.mean_squared_error.__name__ : np.sqrt(metrics.mean_squared_error(actual, pred))
		}

class RQ1(Setup):
	def __init__(self) -> None:
		super().__init__()
	
	def _get_data(self):
		pass

	def _predict(self):
		pass

	def _evaluate(self):
		return self.retrieve_sr_features()

	def __call__(self):
		pass

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
