import typing
import argparse
import numpy as np
import matplotlib.pyplot as plt
plt.style.use("ggplot")

from config import Config
from repohandle import HandleRepo
from sklearn import neural_network, model_selection, metrics, neighbors

parser = argparse.ArgumentParser(description = "Research Questions' Results")
parser.add_argument("-c", "--commit",  type = int, metavar = "", required = False, help = "Enter commit, (5: ABD, 50: DSD)")
parser.add_argument("-t", "--task",  type = str, metavar = "", required = False, help = "Enter task, (SR: Statistic Rep, DR: Neural Rep")
parser.add_argument("-mtp", "--mlptp",  type = str, metavar = "", required = False)
parser.add_argument("-mtlp", "--mlplp",  type = str, metavar = "", required = False)


parser.add_argument("-svp", "--svrtp",  type = str, metavar = "", required = False)
parser.add_argument("-rfp", "--rfrtp",  type = str, metavar = "", required = False)
parser.add_argument("-brp", "--brtp",  type = str, metavar = "", required = False)
parser.add_argument("-knp0", "--knntp0",  type = str, metavar = "", required = False)
parser.add_argument("-knp1", "--knntp1",  type = str, metavar = "", required = False)
parser.add_argument("-h2", "--h2",  type = str, metavar = "", required = False)
parser.add_argument("-rd", "--rdf4j",  type = str, metavar = "", required = False)
parser.add_argument("-db", "--dubbo",  type = str, metavar = "", required = False)
parser.add_argument("-ss", "--systemds",  type = str, metavar = "", required = False)
parser.add_argument("-cb", "--combined",  type = str, metavar = "", required = False)
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
		return [neighbors.KNeighborsRegressor(), neural_network.MLPRegressor()]
	
	def _metrics(self, actual, pred) -> typing.Tuple:
		rmse = np.sqrt(metrics.mean_squared_error(actual, pred))
		mse = metrics.mean_squared_error(actual, pred)
		mae = metrics.mean_absolute_error(actual, pred)
		rmsle = metrics.mean_squared_log_error(actual, pred)
		avg = np.mean([rmse, mse, mae, rmsle])
		return rmse, mse, mae, rmsle, avg

class RQ(Setup):
	def __init__(self) -> None:
		super().__init__()
	
	def _get_data(self):
		return (
			self.retrieve_data_object(self.config.ABD_n, self.config.tgt_pth),
			self.retrieve_data_object(self.config.ABD_n, self.config.AB_sr_pth),
			self.retrieve_data_object(self.config.ABD_n, self.config.AB_nr_pth),
			self.retrieve_data_object(self.config.DSD_n, self.config.tgt_ds_pth),
			self.retrieve_data_object(self.config.DSD_n, self.config.DS_sr_pth),
			self.retrieve_data_object(self.config.DSD_n, self.config.DS_nr_pth)
	  )

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
	
	def _continuous_prediction(self, n, task):
		Xs, ys = self._get_features(n, task)
		predictor = self._predictors()[0]
		out = []
		while True:
			predictor.fit(Xs[n], ys[n])
			out.append(self._metrics(ys[n - 1], predictor.predict(Xs[n - 1])))
			n -= 1
			if n == 1:
				break
		return out
	
	def _plot(self, commits, stat_trt, stat_prt, neural_trt, neural_prt):
		plt.rcParams[self.config.font_family] = self.config.consolas
		fig, ax = plt.subplots()
		ax.plot(commits, stat_trt, label = self.config.sr_trt, color = self.config.p0_color, marker = self.config.star_marker, markerfacecolor = self.config.blk_color)
		ax.plot(commits, stat_prt, label = self.config.sr_prt, color = self.config.p0_color, linestyle = self.config.dash_marker, marker = self.config.star_marker, markerfacecolor = self.config.blk_color)
		ax.plot(commits, neural_trt, label = self.config.nr_trt, color = self.config.p1_color, marker = self.config.o_marker, markerfacecolor = self.config.blk_color)
		ax.plot(commits, neural_prt, label = self.config.nr_prt, color = self.config.p1_color, linestyle = self.config.dash_marker, marker = self.config.o_marker, markerfacecolor = self.config.blk_color)
		ax.legend(fontsize = self.config.base_font)
		plt.xticks(commits, fontsize = self.config.tick_font)
		plt.yticks(fontsize = self.config.tick_font)
		ax.set_ylabel(self.config.time_in_sec, fontsize = self.config.base_font)
		ax.set_xlabel(self.config.commits_nm, fontsize = self.config.base_font)
		plt.legend(fontsize = self.config.base_font)
		plt.tight_layout()
		plt.show()
	
	def _mlp_tp(self):
		mlp, _, _, _, _, _ = self.unpickle(self.config.pred_tp)
		sr_tt, sr_pt, nr_tt, nr_pt = mlp
		self._plot(self.config.commits_ccs, sr_tt, sr_pt, nr_tt, nr_pt)

	def _mlp_lp(self) -> typing.Tuple[float, float, float]:
		mlp, _, _, _, _, _ = self.unpickle(self.config.pred_tp)
		sr_tt, sr_pt, nr_tt, nr_pt = mlp
		sr_ttpt, nr_ttpt = np.mean(sr_tt + sr_pt), np.mean(nr_tt + nr_pt)
		return sr_ttpt, nr_ttpt, np.mean([sr_ttpt, nr_ttpt])

	def _svr_tp(self):
		_, svr, _, _, _, _ = self.unpickle(self.config.pred_tp)
		sr_tt, sr_pt, nr_tt, nr_pt = svr
		self._plot(self.config.commits_ccs, sr_tt, sr_pt, nr_tt, nr_pt)

	def _rfr_tp(self):
		_, _, rfr, _, _, _ = self.unpickle(self.config.pred_tp)
		sr_tt, sr_pt, nr_tt, nr_pt = rfr
		self._plot(self.config.commits_ccs, sr_tt, sr_pt, nr_tt, nr_pt)
	
	def _br_tp(self):
		_, _, _, br, _, _ = self.unpickle(self.config.pred_tp)
		sr_tt, sr_pt, nr_tt, nr_pt = br
		self._plot(self.config.commits_ccs, sr_tt, sr_pt, nr_tt, nr_pt)
	
	def _knn_abd_tp(self):
		_, _, _, _, knn_abd, _ = self.unpickle(self.config.pred_tp)
		sr_tt, sr_pt, nr_tt, nr_pt = knn_abd
		self._plot(self.config.commits_ccs, sr_tt, sr_pt, nr_tt, nr_pt)

	def _knn_dsd_tp(self):
		_, _, _, _, _, knn_dsd = self.unpickle(self.config.pred_tp)
		sr_tt, sr_pt, nr_tt, nr_pt = knn_dsd
		self._plot(self.config.commits_ccs_dsd, sr_tt, sr_pt, nr_tt, nr_pt)

	def _performance(self, sr, y, nr):
		p1, p2 = self._predictors()[0], self._predictors()[0]
		X_train_sr, X_test_sr, y_train, y_test, X_train_nr, X_test_nr = model_selection.train_test_split(sr, y, nr, test_size = self.config.test_size, random_state = self.config.random_state)	
		p1.fit(X_train_sr, y_train), p2.fit(X_train_nr, y_train)
		y_pred_sr, y_pred_nr = p1.predict(X_test_sr), p2.predict(X_test_nr)
		_, sr_mse, _, _, _ = self._metrics(y_test, y_pred_sr)
		_, nr_mse, _, _, _ = self._metrics(y_test, y_pred_nr)
		return {"sr" : sr_mse, "nr": nr_mse}
	
	def _h2(self):
		sr_h2, nr_h2, h2_y = self.unpickle(self.config.sr_h2_X), self.unpickle(self.config.nr_h2_X), self.unpickle(self.config.h2_y)
		return self._performance(sr_h2, h2_y, nr_h2)
	
	def _rdf4j(self):
		sr_rdf4j, nr_rdf4j, rdf4j_y = self.unpickle(self.config.sr_rdf4j_X), self.unpickle(self.config.nr_rdf4j_X), self.unpickle(self.config.rdf4j_y)
		return self._performance(sr_rdf4j, rdf4j_y, nr_rdf4j)
	
	def _dubbo(self):
		sr_dubbo, nr_dubbo, dubbo_y = self.unpickle(self.config.sr_dubbo_X), self.unpickle(self.config.nr_dubbo_X), self.unpickle(self.config.dubbo_y)
		return self._performance(sr_dubbo, dubbo_y, nr_dubbo)
	
	def _systemds(self):
		sr_systemds, nr_systemds, systemds_y = self.unpickle(self.config.sr_systemds_X), self.unpickle(self.config.nr_systemds_X), self.unpickle(self.config.systemds_y)
		return self._performance(sr_systemds, systemds_y, nr_systemds)
	
	def _combined(self):
		sr_combined, nr_combined, combined_y = self.unpickle(self.config.sr_combined_X), self.unpickle(self.config.nr_combined_X), self.unpickle(self.config.combined_y)
		return self._performance(sr_combined, combined_y, nr_combined)

if __name__ == "__main__":
	RQ = RQ()
	if args.commit and args.task:
		print(RQ._continuous_prediction(args.commit, args.task))
	elif args.mlptp:
		RQ._mlp_tp()
	elif args.mlplp:
		print(RQ._mlp_lp()) # 		"-mtlp", "--mlplp",
	elif args.svrtp:
		RQ._svr_tp()
	elif args.rfrtp:
		RQ._rfr_tp()
	elif args.brtp:
		RQ._br_tp()
	elif args.knntp0:
		RQ._knn_abd_tp()
	elif args.knntp1:
		RQ._knn_dsd_tp()
	elif args.h2:
		print(RQ._h2())
	elif args.rdf4j:
		print(RQ._rdf4j())
	elif args.dubbo:
		print(RQ._dubbo())
	elif args.systemds:
		print(RQ._systemds()) 
	elif args.combined:
		print(RQ._combined())