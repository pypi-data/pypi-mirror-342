from d4k_ms_ui.markdown_page import MarkdownPage

class ReleaseNotes(MarkdownPage):
  
  DIR = 'templates/status/partials'
  FILE = 'release_notes.md'

  def __init__(self, dir=None):
    dir = dir if dir else self.DIR
    super().__init__(self.FILE, dir)
    
  def notes(self):
    return self.read()
