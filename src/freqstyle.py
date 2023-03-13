import typing
import numpy as np
from math import isinf
from config import Config
from repohandle import HandleCodeRepo


class FreqStyle(HandleCodeRepo):
	def __init__(self, project = None) -> None:
		super().__init__()
		self.config = Config()
		self.project = project
		self.feature_types = self.config.feature_types
		self.stmt_features = self.feature_types["statements"]
		self.expr_features = self.feature_types["expressions"]
		self.ctrl_features = self.feature_types["controls"]
	
	def _FE(self, source_file, feature, numstat):
		with np.errstate(divide = "ignore"):
			datapoint = -np.log10(feature / self.__len__(source_file))
			numstat.append(0.0) if isinf(datapoint) else numstat.append(datapoint)
	
	def _node_selection(self, tree, features):
		return self.__len__([True for _, node in tree if node.__class__.__name__ in features])

	def __call__(self) -> typing.Tuple[typing.List[str]]:
		self.project = self.config.systemds
		statements, expressions, controls = ([] for _ in range(3))
		source_files, _ = self.get_project(self.project)
		trees, _ = self.get_trees(source_files)
		for tree in trees:
			statements.append(self._node_selection(tree, self.stmt_features))
			expressions.append(self._node_selection(tree, self.expr_features))
			controls.append(self._node_selection(tree, self.ctrl_features))
		numstat_stmts, numstat_expr, numstat_ctrls = ([] for _ in range(3)) 
		for source_file, stmt_feature, expr_feature, ctrl_feature in zip(source_files, statements, expressions, controls):
			self._FE(source_file, stmt_feature, numstat_stmts)
			self._FE(source_file, expr_feature, numstat_expr)
			self._FE(source_file, ctrl_feature, numstat_ctrls)
		
		return {
			"syntactic" : (numstat_stmts, numstat_expr, numstat_ctrls),
			# "lexical" : ()
		}

	def pipeline(self):
		pass

fs = FreqStyle()
print(fs())