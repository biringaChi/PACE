import math
import typing
import numpy as np
from config import Config
from repohandle import HandleRepo

class FreqStyle(HandleRepo):
	"""
	Numerical Statistic Representation of Extracted Code Stylometry Features
	"""
	def __init__(self, project = None) -> None:
		super().__init__()
		self.config = Config()
		self.project = project
		self.feature_types = self.config.feature_types
		self.stmt_features = self.feature_types["statements"]
		self.expr_features = self.feature_types["expressions"]
		self.ctrl_features = self.feature_types["controls"]
		self.invctn_features = self.feature_types["invocations"]
		self.dclrtn_feautes = self.feature_types["declarations"]
	
	def _FE(self, source_file, feature, numstat):
		with np.errstate(divide = "ignore"):
			datapoint = -np.log10(feature / self.__len__(source_file))
			numstat.append(0.0) if math.isinf(datapoint) else numstat.append(datapoint)
	
	def _node_selection(self, tree, features):
		return self.__len__([True for _, node in tree if node.__class__.__name__ in features])

	def __call__(self) -> typing.Dict:
		statements, expressions, controls, invocations, declarations = ([] for _ in range(5))
		source_files = self.get_project(self.project)
		trees, _ = self.get_trees(source_files)
		for tree in trees:
			statements.append(self._node_selection(tree, self.stmt_features))
			expressions.append(self._node_selection(tree, self.expr_features))
			controls.append(self._node_selection(tree, self.ctrl_features))
			invocations.append(self._node_selection(tree, self.invctn_features))
			declarations.append(self._node_selection(tree, self.dclrtn_feautes))
		numstat_stmts, numstat_expr, numstat_ctrls, numstat_invctn, numstat_dclrtn  = ([] for _ in range(5)) 
		for source_file, stmt_feature, expr_feature, ctrl_feature, invctn_feature, dclrtn_feature in zip(
			source_files, 
			statements, 
			expressions, 
			controls,
			invocations, 
			declarations
			):
			self._FE(source_file, stmt_feature, numstat_stmts)
			self._FE(source_file, expr_feature, numstat_expr)
			self._FE(source_file, ctrl_feature, numstat_ctrls)
			self._FE(source_file, invctn_feature, numstat_invctn)
			self._FE(source_file, dclrtn_feature, numstat_dclrtn)
		return {
			"syntactic" : (numstat_stmts, numstat_expr, numstat_ctrls),
			"lexical" : (numstat_invctn, numstat_dclrtn)
		}