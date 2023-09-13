import typing
import argparse
import numpy as np
import matplotlib.pyplot as plt
from config import Config
from repohandle import HandleRepo
from sklearn import neural_network, model_selection, metrics, neighbors

parser = argparse.ArgumentParser(description = "Research Questions' Results")
parser.add_argument("-c", "--commit",  type = int, metavar = "", required = False)
parser.add_argument("-t", "--task",  type = str, metavar = "", required = False)
parser.add_argument("-mtp", "--mlptp",  type = str, metavar = "", required = False)
parser.add_argument("-mtlp", "--mlplp",  type = str, metavar = "", required = False)
parser.add_argument("-svp", "--svrtp",  type = str, metavar = "", required = False)
parser.add_argument("-svlp", "--svrlp",  type = str, metavar = "", required = False)
parser.add_argument("-rfp", "--rfrtp",  type = str, metavar = "", required = False)
parser.add_argument("-rflp", "--rfrlp",  type = str, metavar = "", required = False)
parser.add_argument("-brp", "--brtp",  type = str, metavar = "", required = False)
parser.add_argument("-brlp", "--brlp",  type = str, metavar = "", required = False)
parser.add_argument("-knp0", "--knntp0",  type = str, metavar = "", required = False)
parser.add_argument("-klp0", "--knnlp0",  type = str, metavar = "", required = False)
parser.add_argument("-knp1", "--knntp1",  type = str, metavar = "", required = False)
parser.add_argument("-klp1", "--knnlp1",  type = str, metavar = "", required = False)
parser.add_argument("-abst", "--abslt",  type = str, metavar = "", required = False)
parser.add_argument("-absl", "--absll",  type = str, metavar = "", required = False)
parser.add_argument("-dsdt", "--ddslt",  type = str, metavar = "", required = False)
parser.add_argument("-dsdl", "--ddsll",  type = str, metavar = "", required = False)
parser.add_argument("-absr", "--abdsr",  type = str, metavar = "", required = False)
parser.add_argument("-absrl", "--abdsrl",  type = str, metavar = "", required = False)
parser.add_argument("-abnr", "--abdnr",  type = str, metavar = "", required = False)
parser.add_argument("-abnrl", "--abdnrl",  type = str, metavar = "", required = False)
parser.add_argument("-dssr", "--dsdsr",  type = str, metavar = "", required = False)
parser.add_argument("-dssrl", "--dsdsrl",  type = str, metavar = "", required = False) 
parser.add_argument("-dsnr", "--dsnrsl",  type = str, metavar = "", required = False)
parser.add_argument("-dsnrl", "--dsdnrl",  type = str, metavar = "", required = False)
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
		self.args = args
		plt.style.use("ggplot")
		plt.rcParams[self.config.font_family] = self.config.consolas
		plt.rcParams[self.config.text_color] = self.config.blk_color
		plt.rcParams[self.config.axes_labelcolor] = self.config.blk_color
		plt.rcParams[self.config.xtick_color] = self.config.blk_color
		plt.rcParams[self.config.ytick_color] = self.config.blk_color
	
	def prep_dir(self, ids, dir) ->  typing.Tuple:
		# Prepare feature directories
		return (
			sorted([i + 1 for i in range(ids)], reverse = True),
			sorted([file for file in dir.iterdir() if file.suffix == ".pkl"], reverse = True)
			)

	def retrieve_data_object(self, ids, dir) -> np.ndarray:
		# Get all data objects
		ids, abds = self.prep_dir(ids, dir)
		out = {}  
		for id, abd in zip(ids, abds):
			temp = self.unpickle(abd)
			out[id]  = temp
		return out
	
	def problem_formulation(self, dsd_dir):
		# Problem breakdown for regression model selection, see section 2
		dsd_prep = sorted([file for file in dsd_dir.iterdir() if file.suffix == ".pkl"], reverse = True)
		out = {}
		for path in dsd_prep:
			data, idx = self.unpickle(path), int(str(path).split("-")[-2][2:])
			out[idx] = data
		pass
		
	def _predictors(self):
		return [neighbors.KNeighborsRegressor(), neural_network.MLPRegressor()]
	
	def _metrics(self, actual, pred) -> typing.Tuple:
		# Metrics to measure the predictive prowess of predictors
		rmse = np.sqrt(metrics.mean_squared_error(actual, pred))
		mse = metrics.mean_squared_error(actual, pred)
		mae = metrics.mean_absolute_error(actual, pred)
		rmsle = metrics.mean_squared_log_error(actual, pred)
		avg = np.mean([rmse, mse, mae, rmsle])
		return rmse, mse, mae, rmsle, avg

class RQ(Setup):
	"""
	Answers to research questions
	"""
	def __init__(self) -> None:
		super().__init__()
	
	def _get_data(self):
		return (self.retrieve_data_object(self.config.ABD_n, self.config.tgt_pth), 
	  			self.retrieve_data_object(self.config.ABD_n, self.config.AB_sr_pth), 
				self.retrieve_data_object(self.config.ABD_n, self.config.AB_nr_pth), 
				self.retrieve_data_object(self.config.DSD_n, self.config.tgt_ds_pth), 
				self.retrieve_data_object(self.config.DSD_n, self.config.DS_sr_pth), 
				self.retrieve_data_object(self.config.DSD_n, self.config.DS_nr_pth)
		)
	  
	def _get_features(self, n, task):
		# feature and dataset selection
		if n == 5 and task == "sr":
			ys, Xs, _, _, _, _ = self._get_data()
		elif n == 5 and task == "nr":
			ys, _, Xs, _, _, _ = self._get_data()
		elif n == 50 and task == "sr":
			_, _, _, ys, Xs, _ = self._get_data()
		elif n == 50 and task == "nr":
			_, _, _, ys, _, Xs = self._get_data()
		return Xs, ys
	
	def _continuous_prediction(self, n, snr_fts):
		Xs, ys = self._get_features(n, snr_fts)
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
		# Line graph 1 
		fig, ax = plt.subplots()
		ax.plot(commits, stat_trt, label = self.config.sr_trt, color = self.config.p0_color, marker = self.config.star_marker, markerfacecolor = self.config.blk_color)
		ax.plot(commits, stat_prt, label = self.config.sr_prt, color = self.config.p1_color, linestyle = self.config.dash_marker, marker = self.config.o_marker, markerfacecolor = self.config.blk_color)
		
		ax.plot(commits, neural_trt, label = self.config.nr_trt, color = self.config.p0_color, marker = self.config.star_marker, markerfacecolor = self.config.blk_color)
		ax.plot(commits, neural_prt, label = self.config.nr_prt, color = self.config.p1_color, linestyle = self.config.dash_marker, marker = self.config.o_marker, markerfacecolor = self.config.blk_color)

		# ax.plot(commits, neural_trt, label = self.config.nr_trt, color = self.config.p1_color, marker = self.config.o_marker, markerfacecolor = self.config.blk_color)
		# ax.plot(commits, neural_prt, label = self.config.nr_prt, color = self.config.p1_color, linestyle = self.config.dash_marker, marker = self.config.o_marker, markerfacecolor = self.config.blk_color)
		
		plt.xticks(commits, fontsize = 20, rotation = 45)
		plt.yticks(fontsize = 20)
		plt.locator_params(axis = "x", nbins = 10)
		ax.set_ylabel(self.config.time_in_sec, fontsize = self.config.base_font)
		ax.set_xlabel(self.config.commits_nm, fontsize = self.config.base_font)
		ax.legend(fontsize = self.config.base_font)

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

	def _svr_lp(self) -> typing.Tuple[float, float, float]:
		_, svr, _, _, _, _ = self.unpickle(self.config.pred_tp)
		sr_tt, sr_pt, nr_tt, nr_pt = svr
		sr_ttpt, nr_ttpt = np.mean(sr_tt + sr_pt), np.mean(nr_tt + nr_pt)
		return sr_ttpt, nr_ttpt, np.mean([sr_ttpt, nr_ttpt])

	def _rfr_tp(self):
		_, _, rfr, _, _, _ = self.unpickle(self.config.pred_tp)
		sr_tt, sr_pt, nr_tt, nr_pt = rfr
		self._plot(self.config.commits_ccs, sr_tt, sr_pt, nr_tt, nr_pt)

	def _rfr_lp(self) -> typing.Tuple[float, float, float]:
		_, _, rfr, _, _, _ = self.unpickle(self.config.pred_tp)
		sr_tt, sr_pt, nr_tt, nr_pt = rfr
		sr_ttpt, nr_ttpt = np.mean(sr_tt + sr_pt), np.mean(nr_tt + nr_pt)
		return sr_ttpt, nr_ttpt, np.mean([sr_ttpt, nr_ttpt])
	
	def _br_tp(self):
		_, _, _, br, _, _ = self.unpickle(self.config.pred_tp)
		sr_tt, sr_pt, nr_tt, nr_pt = br
		self._plot(self.config.commits_ccs, sr_tt, sr_pt, nr_tt, nr_pt)

	def _br_lp(self) -> typing.Tuple[float, float, float]:
		_, _, _, br, _, _ = self.unpickle(self.config.pred_tp)
		sr_tt, sr_pt, nr_tt, nr_pt = br
		sr_ttpt, nr_ttpt = np.mean(sr_tt + sr_pt), np.mean(nr_tt + nr_pt)
		return sr_ttpt, nr_ttpt, np.mean([sr_ttpt, nr_ttpt])
	
	def _knn_abd_tp(self):
		_, _, _, _, knn_abd, _ = self.unpickle(self.config.pred_tp)
		sr_tt, sr_pt, nr_tt, nr_pt = knn_abd
		self._plot(self.config.commits_ccs, sr_tt, sr_pt, nr_tt, nr_pt)
	
	def _knn_abd_lp(self) -> typing.Tuple[float, float, float]:
		_, _, _, _, knn_abd, _ = self.unpickle(self.config.pred_tp)
		sr_tt, sr_pt, nr_tt, nr_pt = knn_abd
		sr_ttpt, nr_ttpt = np.mean(sr_tt + sr_pt), np.mean(nr_tt + nr_pt)
		return sr_ttpt, nr_ttpt, np.mean([sr_ttpt, nr_ttpt])

	def _knn_dsd_tp(self):
		_, _, _, _, _, knn_dsd = self.unpickle(self.config.pred_tp)
		sr_tt, sr_pt, nr_tt, nr_pt = knn_dsd
		self._plot(self.config.commits_ccs_dsd2, sr_tt, sr_pt, nr_tt, nr_pt)

	def _knn_dsd_lp(self) -> typing.Tuple[float, float, float]:
		_, _, _, _, _, knn_dsd = self.unpickle(self.config.pred_tp)
		sr_tt, sr_pt, nr_tt, nr_pt = knn_dsd
		sr_ttpt, nr_ttpt = np.mean(sr_tt + sr_pt), np.mean(nr_tt + nr_pt)
		return sr_ttpt, nr_ttpt, np.mean([sr_ttpt, nr_ttpt])
	
	def performance_impact(self, ds_idx = 48) -> typing.Tuple:
		commit = 0
		filters = ["TRT:", "PRT:", "AVG:", "MSE:", "MAE:", "RMSLE:"]
		avg_perf = list(reversed(self.filter_features(self.config.nr_path, filters[2])))
		mse_perf = list(reversed(self.filter_features(self.config.nr_path, filters[3])))
		mae_perf = list(reversed(self.filter_features(self.config.nr_path, filters[4])))
		rmsle_perf = list(reversed(self.filter_features(self.config.nr_path, filters[5])))
		mse_posneg, mae_posneg, rmsle_posneg, avg_posneg = [0], [0], [0], [0]
		commits = [str(("Cn-" + str(i), "Cn-" + str(i + 1))).replace('(','').replace(')','').replace("'", "") for i in range(ds_idx + 1)]
		while commit < ds_idx:
			mse_posneg.append(mse_perf[commit] - mse_perf[commit + 1])
			mae_posneg.append(mae_perf[commit] - mae_perf[commit + 1])
			rmsle_posneg.append(rmsle_perf[commit] - rmsle_perf[commit + 1])
			avg_posneg.append(avg_perf[commit] - avg_perf[commit + 1])
			commit += 1
		return mse_posneg, mae_posneg, rmsle_posneg, avg_posneg, commits
	
	def plot_newRQ(self):
		# revisit
		fig, ax = plt.subplots()
		mse_posneg, mae_posneg, rmsle_posneg, avg_posneg, commits = self.performance_impact()
		colors = ["#760000" if data < 0 else  "#196F3D" for data in avg_posneg]
		plt.hlines(y = commits, xmin = 0, xmax = avg_posneg, color = colors, linewidth = 5)
		
		ax.set_ylabel(self.config.commits_nm, fontsize =  self.config.base_font)
		ax.set_xlabel("Performance Impacts", fontsize =  self.config.base_font)
		plt.xticks(fontsize = 15)
		plt.yticks(commits, fontsize = 15)
	#     plt.locator_params(axis = "y", nbins = 10)
		plt.tight_layout()
		plt.show()

	def _plot1(self, commits, stmt, expr, ctrl, invn, decl):
		fig, ax = plt.subplots()
		ax.plot(commits, stmt, label = self.config.stmt_lab, color = self.config.p0_color, marker = self.config.o_marker, markerfacecolor = self.config.blk_color)
		ax.plot(commits, expr, label = self.config.expr_lab, color = self.config.p1_color, marker = self.config.o_marker, markerfacecolor = self.config.blk_color)
		ax.plot(commits, ctrl, label = self.config.ctrl_lab, color = self.config.p2_color, marker = self.config.o_marker, markerfacecolor = self.config.blk_color)
		ax.plot(commits, invn, label = self.config.invn_lab, color = self.config.p3_color, marker = self.config.o_marker, markerfacecolor = self.config.blk_color)
		ax.plot(commits, decl, label = self.config.decl_lab, color = self.config.p4_color, marker = self.config.o_marker, markerfacecolor = self.config.blk_color)
		ax.legend(fontsize = self.config.base_font)
		# plt.xticks(commits, fontsize = self.config.tick_font)
		# plt.yticks(fontsize = self.config.tick_font)
		
		plt.xticks(commits, fontsize = 20, rotation = 0)
		plt.yticks(fontsize = 20)

		# ax.set_ylabel(self.config.time_in_sec, fontsize = self.config.base_font)
		# ax.set_xlabel(self.config.commits_nm, fontsize = self.config.base_font)

		plt.locator_params(axis = "x", nbins = 5)
		ax.set_ylabel(self.config.time_in_sec, fontsize = self.config.base_font)
		ax.set_xlabel(self.config.commits_nm, fontsize = self.config.base_font)
		plt.legend(fontsize = 20)
		plt.tight_layout()
		plt.show()

	def _abd_selection(self):
		abd_slt, _, _, _, _, _ = self.unpickle(self.config.feature_tp)
		abd_stmt_slt, abd_expr_slt, abd_ctrl_slt, abd_invn_slt, abd_decl_slt = abd_slt
		self._plot1(self.config.commits_ccs1, abd_stmt_slt, abd_expr_slt, abd_ctrl_slt, abd_invn_slt, abd_decl_slt)
	
	def _abd_selection_ssl(self) -> typing.Tuple[float, float, float]:
		abd_slt, _, _, _, _, _ = self.unpickle(self.config.feature_tp)
		abd_stmt_slt, abd_expr_slt, abd_ctrl_slt, abd_invn_slt, abd_decl_slt = abd_slt
		syntactic, lexical = np.mean(abd_stmt_slt + abd_expr_slt + abd_ctrl_slt), np.mean(abd_invn_slt + abd_decl_slt)
		return syntactic, lexical, np.mean([syntactic, lexical])

	def _dsd_selection(self):
		_, dsd_slt, _, _, _, _ = self.unpickle(self.config.feature_tp)
		dsd_stmt_slt, dsd_expr_slt, dsd_ctrl_slt, dsd_invn_slt, dsd_decl_slt = dsd_slt
		self._plot1(self.config.commits_ccs_dsd3, dsd_stmt_slt, dsd_expr_slt, dsd_ctrl_slt, dsd_invn_slt, dsd_decl_slt)
	
	def _dsd_selection_ssl(self) -> typing.Tuple[float, float, float]:
		_, dsd_slt, _, _, _, _ = self.unpickle(self.config.feature_tp)
		dsd_stmt_slt, dsd_expr_slt, dsd_ctrl_slt, dsd_invn_slt, dsd_decl_slt = dsd_slt
		syntactic, lexical = np.mean(dsd_stmt_slt + dsd_expr_slt + dsd_ctrl_slt), np.mean(dsd_invn_slt + dsd_decl_slt)
		return syntactic, lexical, np.mean([syntactic, lexical])
	
	def _abd_sr(self):
		_, _, abd_sr, _, _, _ = self.unpickle(self.config.feature_tp)
		abd_sr_stmt, abd_sr_expr, abd_sr_ctrl, abd_sr_invn, abd_sr_decl = abd_sr
		self._plot1(self.config.commits_ccs1, abd_sr_stmt, abd_sr_expr, abd_sr_ctrl, abd_sr_invn, abd_sr_decl)
	
	def _abd_sr_ssl(self) -> typing.Tuple[float, float, float]:
		_, _, abd_sr, _, _, _ = self.unpickle(self.config.feature_tp)
		abd_sr_stmt, abd_sr_expr, abd_sr_ctrl, abd_sr_invn, abd_sr_decl = abd_sr
		syntactic, lexical = np.mean(abd_sr_stmt + abd_sr_expr + abd_sr_ctrl), np.mean(abd_sr_invn + abd_sr_decl)
		return syntactic, lexical, np.mean([syntactic, lexical])

	def _abd_nr(self):
		_, _, _, abd_nr, _, _ = self.unpickle(self.config.feature_tp)
		abd_nr_stmt, abd_nr_expr, abd_nr_ctrl, abd_nr_invn, abd_nr_decl = abd_nr
		self._plot1(self.config.commits_ccs1, abd_nr_stmt, abd_nr_expr, abd_nr_ctrl, abd_nr_invn, abd_nr_decl)
	
	def _abd_nr_ssl(self) -> typing.Tuple[float, float, float]:
		_, _, _, abd_nr, _, _ = self.unpickle(self.config.feature_tp)
		abd_nr_stmt, abd_nr_expr, abd_nr_ctrl, abd_nr_invn, abd_nr_decl = abd_nr
		syntactic, lexical = np.mean(abd_nr_stmt + abd_nr_expr + abd_nr_ctrl), np.mean(abd_nr_invn + abd_nr_decl)
		return syntactic, lexical, np.mean([syntactic, lexical])

	def _dsd_sr(self):
		_, _, _, _, dsd_sr_rep, _ = self.unpickle(self.config.feature_tp)
		dsd_sr_stmt, dsd_sr_expr, dsd_sr_ctrl, dsd_sr_invn, dsd_sr_decl = dsd_sr_rep
		self._plot1(self.config.commits_ccs_dsd3, dsd_sr_stmt, dsd_sr_expr, dsd_sr_ctrl, dsd_sr_invn, dsd_sr_decl)

	def _dsd_sr_ssl(self) -> typing.Tuple[float, float, float]:
		_, _, _, _, dsd_sr_rep, _ = self.unpickle(self.config.feature_tp)
		dsd_sr_stmt, dsd_sr_expr, dsd_sr_ctrl, dsd_sr_invn, dsd_sr_decl = dsd_sr_rep
		syntactic, lexical = np.mean(dsd_sr_stmt + dsd_sr_expr + dsd_sr_ctrl), np.mean(dsd_sr_invn + dsd_sr_decl)
		return syntactic, lexical, np.mean([syntactic, lexical])
	
	def _dsd_nr(self):
		_, _, _, _, _, dsd_nr_rep = self.unpickle(self.config.feature_tp)
		dsd_nr_stmt, dsd_nr_expr, dsd_nr_ctrl, dsd_nr_invn, dsd_nr_decl = dsd_nr_rep
		self._plot1(self.config.commits_ccs_dsd3, dsd_nr_stmt, dsd_nr_expr, dsd_nr_ctrl, dsd_nr_invn, dsd_nr_decl)

	def _dsd_nr_ssl(self) -> typing.Tuple[float, float, float]:
		_, _, _, _, _, dsd_nr_rep = self.unpickle(self.config.feature_tp)
		dsd_nr_stmt, dsd_nr_expr, dsd_nr_ctrl, dsd_nr_invn, dsd_nr_decl = dsd_nr_rep
		syntactic, lexical = np.mean(dsd_nr_stmt + dsd_nr_expr + dsd_nr_ctrl), np.mean(dsd_nr_invn + dsd_nr_decl)
		return syntactic, lexical, np.mean([syntactic, lexical])

	def _performance(self, sr, y, nr):
		# Predictor testing 
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
	
	def __call__(self):
		if args.commit and args.task:
			print(self._continuous_prediction(args.commit, args.task))
		elif args.mlptp:
			self._mlp_tp()
		elif args.mlplp:
			print(self._mlp_lp())
		elif args.svrtp:
			self._svr_tp()
		elif args.svrlp:
			print(self._svr_lp())
		elif args.rfrtp:
			self._rfr_tp()
		elif args.rfrlp:
			print(self._rfr_lp())
		elif args.brtp:
			self._br_tp()
		elif args.brlp:
			print(self._br_lp())
		elif args.knntp0:
			self._knn_abd_tp()
		elif args.knnlp0:
			print(self._knn_abd_lp())
		elif args.knntp1:
			self._knn_dsd_tp()
		elif args.knnlp1:
			print(self._knn_dsd_lp())
		elif args.abslt:
			self._abd_selection()
		elif args.absll:
			print(self._abd_selection_ssl()) 
		elif args.ddslt:
			self._dsd_selection()
		elif args.ddsll:
			print(self._dsd_selection_ssl())
		elif args.abdsr:
			self._abd_sr()
		elif args.abdsrl:
			print(self._abd_sr_ssl())
		elif args.abdnr:
			self._abd_nr()
		elif args.abdnrl:
			print(self._abd_nr_ssl())
		elif args.dsdsr:
			self._dsd_sr()
		elif args.dsdsrl:
			print(self._dsd_sr_ssl())
		elif args.dsnrsl:
			self._dsd_nr()
		elif args.dsdnrl:
			print(self._dsd_nr_ssl())
		elif args.h2:
			print(self._h2())
		elif args.rdf4j:
			print(self._rdf4j())
		elif args.dubbo:
			print(self._dubbo())
		elif args.systemds:
			print(self._systemds()) 
		elif args.combined:
			print(self._combined())

if __name__ == "__main__":
	RQ().__call__()