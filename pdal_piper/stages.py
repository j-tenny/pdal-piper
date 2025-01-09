class _GenericStage:
  def __init__(self,name, **kwargs):
      if 'classification' in kwargs.keys():
          kwargs['class'] = kwargs['classification']
          del (kwargs['classification'])
      self.name = name
      self.args = tuple(kwargs.items())
      self.args = tuple([arg for arg in self.args if (arg[1] is not None)])

