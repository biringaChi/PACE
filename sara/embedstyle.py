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
		self.seqlen = self.cfg.max_seqlen
		self.ft = self.cfg.feature_types
		self.features = self.ft["statements"] + self.ft["expressions"] + self.ft["controls"] + self.ft["invocations"] + self.ft["declarations"]
	
	def _node_selection(self, tree):
		return [node.__class__.__name__ for _, node in tree if node.__class__.__name__ in self.features]

	def _model(data, vec_id):
		vectors = Word2Vec(sentences = data, vector_size = 32).wv
		vectors.save(pathlib.Path.cwd().parents[0]/"embeddings"/vec_id)
	
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
		return [vector[:self.seqlen] if self.__len__(vector) > self.seqlen else vector for vector in embeddings] 
		
	def _zeropad(self, embeddings):
		out  = []		
		for embedding in embeddings:
			if len(embedding) < self.seqlen:
				embedding.extend([0.0] * (self.seqlen - len(embedding)))
		for embedding in embeddings:
			temp = []
			for vector in embedding:
				if not type(vector).__module__ == np.__name__:
					temp.append(np.zeros((32,), dtype = np.float64))
				else: temp.append(vector)
			out.append(temp)
		return out

	def _store_vectors(self, vector):
		pass

	def _load_vectors(self, vector):
		pass
		
	def __call__(self):
		source_files = self.get_project(self.project)
		trees, _ = self.get_trees(source_files)
		features = [self._node_selection(tree) for tree in trees]
		observations = self._model(features, "vectors.kv")
		embeddings = self._vector_match(observations)
		embeddings = self._truncate(embeddings)
		embeddings = self._zeropad(embeddings)
		return embeddings