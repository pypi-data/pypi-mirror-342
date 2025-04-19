from d4k_ms_ui.markdown_page import MarkdownPage

def test_create_no_dir(mocker):
  mp = MarkdownPage('filename.abc')
  assert mp is not None
  assert mp._dir == MarkdownPage.DIR
  assert mp._text == None
  assert mp._filename == 'filename.abc'

def test_create_dir(mocker):
  mp = MarkdownPage('someother.txt', 'some/path')
  assert mp is not None
  assert mp._dir == 'some/path'
  assert mp._text == None
  assert mp._filename == 'someother.txt'

def test_read(mocker):
  mock_read = mocker.patch('d4k_ms_ui.release_notes.MarkdownPage._read')
  mock_read.side_effect = ['test1234']
  mp = MarkdownPage('someother.txt', 'some/path')
  assert mp.read() == '<p>test1234</p>'

def test__read(mocker):
  mocker.patch('builtins.open', mocker.mock_open(read_data='test'))  
  mp = MarkdownPage('someother.txt', 'some/path')
  result = mp._read('path')
  assert result == 'test'
