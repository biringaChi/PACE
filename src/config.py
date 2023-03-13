import typing
import pathlib

class Config:
	"""
	Configurations
	"""
	def __init__(self) -> None:
		self.pth = pathlib.Path.cwd().parents[0]/"datasets/tep-gnn/JavaTestFiles"
		self.h2_repo = self.pth/"H2"
		self.rdf4j_repo = self.pth/"rdf4j"
		self.dubbo = self.pth/"apache/dubbo"
		self.systemds = self.pth/"apache/systemds"

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