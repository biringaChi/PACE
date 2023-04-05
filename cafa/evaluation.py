# from config import Config
# from freqstyle import FreqStyle
# from repohandle import HandleRepo

class Evaluation:
	def __init__(self) -> None:
		pass

	def __call__(self) -> None:
		cross_validation_metrics = {
			"rmse" : "neg_root_mean_squared_error", "mse" : "neg_mean_squared_error", 
			"rmsle" : "neg_mean_squared_log_error", "mae" : "neg_mean_absolute_error"
		}
		testing_metric = {
			
		}