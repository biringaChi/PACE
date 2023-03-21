import typing
import pathlib
import numpy as np
from config import Config
from repohandle import HandleRepo
from gensim.models import Word2Vec, KeyedVectors

class EmbedStyle(HandleRepo):
	"""
	Distributional Semantic Representation of Extracted Code Stylometry Features 
	"""
	def __init__(self, project = None) -> None:
		super().__init__()
		self.cfg = Config()
		self.ft = self.cfg.ft
		self.features = self.ft["statements"] + self.ft["expressions"] + self.ft["controls"] + self.ft["invocations"] + self.ft["declarations"]

	def _model(data, vec_name):
		vectors = Word2Vec(sentences = data, vector_size = 32).wv
		vectors.save(pathlib.Path.cwd().parents[0]/"embeddings"/vec_name)
	
	def _vector_match(vectors, observations):
		vec_dict = {}
		model = KeyedVectors.load(vectors, mmap = "r")
		for key in model.key_to_index.keys():
			vec_dict[key] = model[key]
		embeddings = []
		for embeds in observations:
			temp = []
			for embed in embeds:
				if embed in vec_dict:
					temp.append(vec_dict[embed])
			embeddings.append(temp)
		return embeddings
	
	def _truncate(self, embeddings):
		out = []
		for embedding in embeddings:
			out.append(embedding[:self.cfg.seq_size]) if len(embedding) > self.cfg.seq_size else out.append(embedding)
		return out

	def _zeropad(self, embeddings):
		zeros: np.ndarray = np.zeros((32,), dtype = np.float64)
		out  = []
		max_length: int = max(self.__len__(embedding) for embedding in embeddings)
		for embedding in embeddings:
			if len(embedding) < max_length:
				embedding.extend([0.0] * (max_length - self.__len__(embedding)))
		for embedding in embeddings:
			temp = []
			for vector in embedding:
				if not type(vector).__module__ == np.__name__:
					temp.append(zeros)
				else: temp.append(vector)
			out.append(temp)
		return out

	def _store_object(self):
		pass

	def _load_object(self):
		pass

	def _1D_convert(sef):
		pass
		
	def __call__(self):
		source_files = self.get_project(self.project)
		trees, _ = self.get_trees(source_files)
		features = []
		for tree in trees:
			features.append([node.__class__.__name__ for _, node in tree if node.__class__.__name__ in self.features])
		return features