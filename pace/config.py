import typing
import pathlib

class Config:
	"""
	Configurations
	"""
	def __init__(self) -> None:
		self.pth: str = pathlib.Path.cwd().parents[0]/"datasets/tep-gnn/JavaTestFiles"
		self.h2: str = self.pth/"H2"
		self.rdf4j: str = self.pth/"rdf4j"
		self.dubbo: str = self.pth/"apache/dubbo"
		self.systemds: str = self.pth/"apache/systemds"
		self.ftr_pth = pathlib.Path.cwd() / "features/"
		self.AB_sr_pth = self.ftr_pth / "AB/SR"
		self.AB_nr_pth = self.ftr_pth / "AB/NR"
		self.DS_sr_pth = self.ftr_pth / "DS/SR"
		self.DS_nr_pth = self.ftr_pth / "DS/NR"
		self.sota = self.ftr_pth / "SOTA"
		self.pred_tp = self.ftr_pth / "throughput/predictor_timecost.pkl"
		self.feature_tp = self.ftr_pth / "throughput/features_timecost.pkl"
		self.sr_dubbo_X = self.sota / "SR/SR_dubbo_X.pkl"
		self.sr_h2_X = self.sota / "SR/SR_h2_X.pkl"
		self.sr_rdf4j_X = self.sota / "SR/SR_rdf4j_X.pkl"
		self.sr_systemds_X = self.sota / "SR/SR_systemds_X.pkl"
		self.sr_combined_X = self.sota / "SR/SR_combined_X.pkl"
		self.nr_dubbo_X = self.sota / "NR/NR_dubbo_X.pkl"
		self.nr_h2_X = self.sota / "NR/NR_h2_X.pkl"
		self.nr_rdf4j_X = self.sota / "NR/NR_rdf4j_X.pkl"
		self.nr_systemds_X = self.sota / "NR/NR_systemds_X.pkl"
		self.nr_combined_X = self.sota / "NR/NR_combined_X.pkl"
		self.dubbo_y = self.sota / "targets/dubbo_y.pkl"
		self.h2_y = self.sota / "targets/h2_y.pkl"
		self.NR_h2_y = self.sota / "targets/NR_h2_y.pkl"
		self.rdf4j_y = self.sota / "targets/rdf4j_y.pkl"
		self.systemds_y = self.sota / "targets/systemds_y.pkl"
		self.combined_y = self.sota / "targets/combined_y.pkl"
		self.base_font = 25
		self.sr_trt = "SR-Training"
		self.sr_prt = "SR-Prediction"
		self.nr_trt = "NR-Training"
		self.nr_prt = "NR-Prediction" 
		self.stmt_lab = "Statements"
		self.expr_lab = "Expressions"
		self.ctrl_lab = "Controls"
		self.invn_lab = "Invocations"
		self.decl_lab = "Declarations"
		self.tick_font = 15
		self.p0_color = "#760000"
		self.p1_color = "#196F3D"
		self.p2_color = "#19485c"
		self.p3_color = "#d8d827"
		self.p4_color = "#6c006c"
		self.blk_color = "#000000"
		self.star_marker = "*"
		self.dash_marker = "--"
		self.o_marker = "o"
		self.consolas = "Consolas"
		self.commits_nm = "Commits"
		self.commits_ccs = ["Cn-" + str(i + 1) for i in range(4)]
		self.commits_ccs1 = ["Cn-" + str(i + 1) for i in range(5)]
		self.commits_ccs_dsd = [str(i + 1) for i in range(49)]
		self.commits_ccs_dsd1 =  [str(i + 1) for i in range(50)]
		self.time_in_sec = "Time (seconds)"
		self.font_family = "font.family"
		self.ABD_n = 5
		self.random_state = 4
		self.test_size = 0.2
		self.DSD_n = 50
		self.tgt_pth = self.ftr_pth / "AB/targets"
		self.tgt_ds_pth = self.ftr_pth / "DS/targets"
		self.runtime_c = "Test File;Runtime in ms"
		self.runtime_c_ms = "Runtime in ms"
		self.dubbo_h2 = "dubbo|h2"
		self.rdf4j = "rdf4j"
		self.file_name = "file_name"
		self.runtime_ms = "runtime_ms"
		self.test_case = "Test case"
		self.test_file = "Test File"
		self.max_seqlen: int = 64
		self.feature_types: typing.Dict =  {
			"statements" : [
				"IfStatement", "WhileStatement", "DoStatement",
				"AssertStatement", "SwitchStatement", "ForStatement",
				"ContinueStatement", "ReturnStatement", "ThrowStatement",
				"SynchronizedStatement", "TryStatement", "BreakStatement",
				"BlockStatement", "BinaryOperation", "CatchClause"
			],
			"expressions" : [
				"StatementExpression", "TernaryExpression", "LambdaExpression"
			],
			"controls" : [
				"ForControl", "EnhancedForControl"
			],
			"invocations" : [
				"SuperConstructorInvocation", "MethodInvocation",  "SuperMethodInvocation", "SuperMemberReference"
				"ExplicitConstructorInvocation", "ArraySelector", "AnnotationMethod", "MethodReference"
			],
			"declarations" : [
				"TypeDeclaration", "FieldDeclaration", "MethodDeclaration", 
				"ConstructorDeclaration", "PackageDeclaration", "ClassDeclaration", 
				"EnumDeclaration", "InterfaceDeclaration", "AnnotationDeclaration", 
				"ConstantDeclaration", "VariableDeclaration", "LocalVariableDeclaration",
				"EnumConstantDeclaration", "VariableDeclarator"
			]
	}