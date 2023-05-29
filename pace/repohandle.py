import os
import re
import pathlib
import javalang
import pickle
import pandas as pd
from config import Config
from javalang.tree import CompilationUnit
from javalang.parser import JavaSyntaxError
from typing import Tuple, Dict, List, Sequence, Set, Text, Union

class HandleRepo:
	def __init__(self) -> None:
		self.config = Config()

	def __len__(self, arg: Union[Sequence, Text, Dict, Set]) -> int:
		if (isinstance(arg, (int, float, bool))):
			raise TypeError("Invalid argument. Only text, sequence, mapping and set are accepted")
		else:
			return len(arg)

	def pickle(self, data, file_name):
		with open(file_name, "wb") as file:
			pickle.dump(data, file)
	
	def unpickle(self, data):
		with open(data, "rb") as file:
			loaded = pickle.load(file)
		return loaded

	def get_trees(self, source_files) -> CompilationUnit:
		trees = []
		uncompiled_sourcecode = {}
		for idx, sourcecode in enumerate(source_files):
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

	def get_runtime(self, runtime_path: Union[str, Tuple[str, str]]) -> List[float]:
		runtime: pd.DataFrame = pd.read_csv(runtime_path)
		file_id = runtime_path.split("/")[-1].lower()
		if re.search(self.config.dubbo_h2, file_id):
			file_name = runtime[self.config.runtime_c].apply(lambda x:x.split(";")[0]).apply(lambda x:x.split(".")[-1])
			runtime_ms = runtime[self.config.runtime_c].apply(lambda x:x.split(";")[1])
			return pd.DataFrame({self.config.file_name:file_name, self.config.runtime_ms:runtime_ms})
		elif re.search(self.config.rdf4j, file_id):
			return pd.DataFrame({self.config.file_name:runtime[self.config.test_case], self.config.runtime_ms:runtime[self.config.runtime_c_ms]})
		else:
			runtime: pd.DataFrame = pd.concat([pd.read_csv(runtime_path[0]), pd.read_csv(runtime_path[1])])
			return pd.DataFrame({self.config.file_name: runtime[self.config.test_file], self.config.runtime_ms:runtime[self.config.runtime_c_ms]})