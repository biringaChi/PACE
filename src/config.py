import typing
import pathlib

class Config:
	"""
	Configurations
	"""
	def __init__(self) -> None:
		self.pth = pathlib.Path.cwd().parents[0]/"datasets/tep-gnn/JavaTestFiles"
		self.h2 = self.pth/"H2"
		self.rdf4j = self.pth/"rdf4j"
		self.dubbo = self.pth/"apache/dubbo"
		self.systemds = self.pth/"apache/systemds"
		self.runtime_c = "Test File;Runtime in ms"
		self.runtime_c_ms = "Runtime in ms"
		self.dubbo_h2 = "dubbo|h2"
		self.rdf4j = "rdf4j"
		self.file_name = "file_name"
		self.runtime_ms = "runtime_ms"
		self.test_case = "Test case"
		self.test_file = "Test File"

		self.feature_types: typing.Dict =  {
			"statements" : {
				"IfStatement", "WhileStatement", "DoStatement",
				"AssertStatement", "SwitchStatement", "ForStatement",
				"ContinueStatement", "ReturnStatement", "ThrowStatement",
				"SynchronizedStatement", "TryStatement", "BreakStatement",
				"BlockStatement", "BinaryOperation", "CatchClause"
				},
			"expressions" : {
				"StatementExpression", "TernaryExpression", "LambdaExpression"
				},
			"controls" : {
				"ForControl", "EnhancedForControl"
			},
			"invocations" : {
				"SuperConstructorInvocation", "MethodInvocation",  "SuperMethodInvocation", "SuperMemberReference"
				"ExplicitConstructorInvocation", "ArraySelector", "AnnotationMethod", "MethodReference"
				},
			"declarations" : {
				"TypeDeclaration", "FieldDeclaration", "MethodDeclaration", 
				"ConstructorDeclaration", "PackageDeclaration", "ClassDeclaration", 
				"EnumDeclaration", "InterfaceDeclaration", "AnnotationDeclaration", 
				"ConstantDeclaration", "VariableDeclaration", "LocalVariableDeclaration",
				"EnumConstantDeclaration", "VariableDeclarator"
				}
		}