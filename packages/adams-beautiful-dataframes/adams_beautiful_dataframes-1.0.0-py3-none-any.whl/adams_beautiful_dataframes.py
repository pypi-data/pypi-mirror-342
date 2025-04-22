def load_ipython_extension(ipython):
  from IPython.core.display import HTML

  def hook(result):
    display(HTML('<style>table { font-family: "Comic Sans MS"; }</style>'))
    # ipython.events.unregister('post_run_cell', hook)

  ipython.events.register('post_run_cell', hook)

def unload_ipython_extension(ipython):
  pass


def install():
  from pathlib import Path

  try:
    from IPython.paths import get_ipython_dir
  except ImportError:
    return

  path = Path(get_ipython_dir()) / 'profile_default/startup/adams_beautiful_dataframes.py'
  path.write_text('''try:
  import adams_beautiful_dataframes
except ImportError:
  pass
else:
  get_ipython().run_line_magic('load_ext', 'adams_beautiful_dataframes')
''')
