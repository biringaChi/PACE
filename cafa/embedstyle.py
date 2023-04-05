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
		self.project = project
		self.seqlen = self.cfg.max_seqlen
		self.ft = self.cfg.feature_types
		self.features = self.ft["statements"] + self.ft["expressions"] + self.ft["controls"] + self.ft["invocations"] + self.ft["declarations"]
	
	def node_selection(self, tree) -> typing.List:
		return [node.__class__.__name__ for _, node in tree if node.__class__.__name__ in self.features]

	def model(data, vec_id):
		vectors = Word2Vec(sentences = data, vector_size = 32).wv
		vectors.save(pathlib.Path.cwd().parents[0]/"embeddings"/vec_id)
	
	def vector_match(vectors, observations):  
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
	
	def truncate(self, embeddings):
		return [vector[:self.seqlen] if self.__len__(vector) > self.seqlen else vector for vector in embeddings] 
		
	def zeropad(self, embeddings):
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
	
	def flatten(self, embeddings):
		out = []
		for embedding in embeddings:
			if not embedding:
				out.append(embedding)
			else:
				flatten_list = np.concatenate(embedding).ravel().tolist()
				out.append(flatten_list) 
		return out
			
	def __call__(self):
		trees, _ = self.get_trees(self.get_project(self.project))
		features = [self.node_selection(tree) for tree in trees]
		return self.zeropad(self.truncate(self.vector_match(self.model(features, "vectors.kv")))) #os.getdir