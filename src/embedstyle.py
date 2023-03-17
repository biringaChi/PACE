from config import Config
from freqstyle import FreqStyle

class EmbedStyle(FreqStyle):
	"""
	"""
	def __init__(self, project = None) -> None:
		super().__init__()
		self.config = Config()
		print()