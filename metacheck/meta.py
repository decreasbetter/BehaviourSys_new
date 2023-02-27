class Meta():

    def __init__(self, cfg) -> None:
        self.meta = cfg.meta
        self.spatial_relation = cfg.spatial_relation
        self.temporal_relation = cfg.temporal_relation

    def check(self, obj):
        pass