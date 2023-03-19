import typing
import pathlib
from config import Config
from repohandle import HandleRepo
from gensim.models import Word2Vec, KeyedVectors

class EmbedStyle(HandleRepo):
	"""
	Distributional Semantic Representation of Extracted Code Stylometry Features 
	"""
	def __init__(self, project = None) -> None:
		super().__init__()
		self.config = Config()
		self.ft = self.config.ft
		self.features = self.ft["statements"] + self.ft["expressions"] + self.ft["controls"] + self.ft["invocations"] + self.ft["declarations"]

	def _model(data, vec_name):
		vectors = Word2Vec(sentences = data, vector_size = 32).wv
		vectors.save(pathlib.Path.cwd().parents[0]/"embeddings"/vec_name)
	
	def _vectors_match(vectors, observations):
		vec_dict = {}
		model = KeyedVectors.load(vectors, mmap = "r")
		for key in model.key_to_index.keys():
			vec_dict[key] = model[key]
		out = []
		for embeds in observations:
			temp = []
			for embed in embeds:
				if embed in vec_dict:
					temp.append(vec_dict[embed])
			out.append(temp)
		return out
		
	def __call__(self):
		source_files = self.get_project(self.project)
		trees, _ = self.get_trees(source_files)
		out = []
		for tree in trees:
			out.append([node.__class__.__name__ for _, node in tree if node.__class__.__name__ in self.features])
		return out