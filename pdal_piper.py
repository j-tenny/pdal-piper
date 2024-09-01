class Piper:
    def __init__(self):
        self.pipeline = []
    def add_stage(self,stage_name,**kwargs):
        self.pipeline