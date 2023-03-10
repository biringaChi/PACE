import os
import re
import pathlib
import javalang
import pandas as pd
from pandas.core.frame import DataFrame
from javalang.tree import CompilationUnit
from javalang.parser import JavaSyntaxError
from typing import Tuple, Dict, List, Sequence, Set, Text, Union

class HandleCodeRepo:
	def __init__(self) -> None:
		self.path = pathlib.Path.cwd()
		print(self.path)
		# self.h2 = self.path / ""

	@property
	def _GET_DATA_DIR(self) -> List[str]:
		datasets = {"AddressBook" : "addressbook.csv", "DSpace" : "dspace.csv"} 
		return os.path.join("./dataset", datasets.get("DSpace"))

	def __str__(self) -> str:
		return f"{self.__class__.__name__}({self._GET_DATA_DIR})"

	def __repr__(self) -> str:
		return self.__str__()
	
	def __len__(self, arg: Union[Sequence, Text, Dict, Set]) -> int:
		if (isinstance(arg, (int, float, bool))):
			raise TypeError("Invalid argument. Only text, sequence, mapping and set are accepted")
		else:
			return len(arg)
	
	def node_types(self) -> Union[Dict[str, List[str]], str, List[str]]:
		return {
			"declaration" : {
				"TypeDeclaration", "FieldDeclaration", "MethodDeclaration", 
				"ConstructorDeclaration", "PackageDeclaration", "ClassDeclaration", 
				"EnumDeclaration", "InterfaceDeclaration", "AnnotationDeclaration", 
				"ConstantDeclaration", "VariableDeclaration", "LocalVariableDeclaration",
				"EnumConstantDeclaration"
				},
			"statement" : {
				"IfStatement", "WhileStatement", "DoStatement",
				"AssertStatement", "SwitchStatement", "ForStatement",
				"ContinueStatement", "ReturnStatement", "ThrowStatement",
				"SynchronizedStatement", "TryStatement", "BreakStatement",
				"BlockStatement"
				},
			"expression" : {
				"StatementExpression", "TernaryExpression", "LambdaExpression"
				},
			"invocation" : {
				"SuperConstructorInvocation", "MethodInvocation",  "SuperMethodInvocation",
				"ExplicitConstructorInvocation"
				},
			"other" : {
				"ForControl", "EnhancedForControl", "FormalParameter",
				"AnnotationMethod", "VariableDeclarator", "CatchClause",
				"BinaryOperation", "MethodReference", "ArraySelector",
				"SuperMemberReference"
				},
			}

	def read_data(self) -> DataFrame:
		try:
			return pd.read_csv(self._GET_DATA_DIR)
		except FileNotFoundError as e:
			raise(e)
	
	def get_version(self) -> List[str]:
		return [version for version in self.read_data()["version"]]
	
	def get_build(self) -> List[str]:
		return [build for build in self.read_data()["build"]]
	
	def get_test(self) -> List[float]:
		return [test for test in self.read_data()["test"]]

	def get_hash(self) -> List[str]:
		return [hash for hash in self.read_data()["hash"]]

	def get_sourcecode(self) -> str:
		return [code for code in self.read_data()["sourcecode"]]

	def get_unit_test(self) -> List[float]:
		return [code for code in self.read_data()["unit_test"]] 

	def get_integration_test(self) -> List[float]:
		return [code for code in self.read_data()["integration_test"]]

	def get_unit_integration_test(self) -> List[float]:
		return [code for code in self.read_data()["unit_integration_test"]]

	def get_trees(self, code):
		trees = []
		uncompiled_sourcecode = {}
		for idx, sourcecode in enumerate(code):
			try:
				trees.append(javalang.parse.parse(sourcecode))
			except JavaSyntaxError as e:
				uncompiled_sourcecode[idx] = sourcecode
				trees.append(None)
		return trees, uncompiled_sourcecode

	def get_project(self, project) -> Tuple[List[str], List[str]]:
		source_files, source_file_names = [], []
		for root, _, files in os.walk(project):
			for file in files:
				if file.endswith(".java"):
					temp = os.path.join(root, file)
					source_file_names.append(pathlib.Path(temp).stem)
					try:
						with open(temp, "r") as source_file:
							source_files.append(source_file.read())
					except OSError as e:
						raise e
		return source_files, source_file_names

	def get_runtime(self, runtime_path: Union[str, Tuple[str, str]]):
		runtime: pd.DataFrame = pd.read_csv(runtime_path)
		file_id = runtime_path.split("/")[-1].lower()
		if re.search("dubbo|h2", file_id):
			file_name = runtime["Test File;Runtime in ms"].apply(lambda x: x.split(";")[0]).apply(lambda x: x.split(".")[-1])
			runtime_ms = runtime["Test File;Runtime in ms"].apply(lambda x: x.split(";")[1])
			return pd.DataFrame({"file_name": file_name, "runtime_ms": runtime_ms})
		elif re.search("rdf4j", file_id):
			return pd.DataFrame({"file_name": runtime["Test case"], "runtime_ms": runtime["Runtime in ms"]})
		else:
			runtime: pd.DataFrame = pd.concat([pd.read_csv(runtime_path[0]), pd.read_csv(runtime_path[1])])
			return pd.DataFrame({"file_name": runtime["Test File"], "runtime_ms": runtime["Runtime in ms"]})