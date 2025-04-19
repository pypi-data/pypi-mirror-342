import os
import markdown

class MarkdownPage:
  
  DIR = 'templates/markdown/partials'

  def __init__(self, filename: str, dir: str=None):
    self._filename = filename
    self._dir = dir if dir else self.DIR
    self._text = None

  def read(self) -> str:
    path = os.path.join(self._dir, self._filename)
    self._text = self._read(path)
    return markdown.markdown(self._text)
  
  def _read(self, fullpath: str) -> str:
    with open(fullpath, "r") as f:
      return f.read()
