from d4k_ms_ui.release_notes import ReleaseNotes

def test_create_no_dir(mocker):
  rn = ReleaseNotes()
  assert rn is not None
  assert rn._dir == ReleaseNotes.DIR
  assert rn._text == None

def test_create_dir(mocker):
  rn = ReleaseNotes('some/path')
  assert rn is not None
  assert rn._dir == 'some/path'
  assert rn._text == None

def test_notes(mocker):
  mocker.patch('builtins.open', mocker.mock_open(read_data='test'))  
  rn = ReleaseNotes('some/path')
  assert rn.notes() == '<p>test</p>'
