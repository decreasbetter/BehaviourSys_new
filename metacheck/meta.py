class Meta():

    def __init__(self, cfg) -> None:
        self.meta = cfg.meta
        self.spatial_relation = cfg.spatial_relation
        self.temporal_relation = cfg.temporal_relation

        self.cur_sate = 0  # 时间上，当前进行的基元-基元-关系
        self.behaviour_state = False  # 该周期的操作规范标识符，周期结束时判断
        self.op_ing = False  # 操作状态标识符

    def reset(self):
        self.cur_sate = 0
        self.behaviour_state = False

    def update(self, meta_info):
        """
        meta_info: 字典{objInfo类}
        """
        if 'hand' in meta_info:
            # 手出现在操作区域内时，属于操作中，进行基元关系检测
            if not self.op_ing:
                self.reset()
            self.op_ing = True  
            state_idx = self.temporal_relation[self.cur_sate]  # 当前操作的基元关系索引
            
            # 判断当前的操作基元关系是否出现
            state = False
            for idx in state_idx:
                meta_state = self.spatial_relation[idx]
                meta_state = meta_state.split('-')
                for meta1 in meta_info[meta_state[0]]:
                    for meta2 in meta_info[meta_state[1]]:
                        state |= self.check(meta1, meta2, meta_state[2])
            # 若当前基元关系已出现，则进行下一基元关系检测
            if state:
                self.cur_sate += 1
        else:
            # 手不在操作区域时，说明不在操作状态
            self.op_ing = False
            if self.cur_sate == len(self.temporal_relation):
                self.behaviour_state = True
            else:
                self.behaviour_state = False

    def check(self, meta1, meta2, spa_relation):
        """
        meta1, meta2: 两个基元类obfInfo
        spa_relation: 两基元之间的关系
        """
        
        if spa_relation == 'concate':
            relation = meta1.isConcate(meta2)
        elif spa_relation == 'depart':
            relation = meta1.isDepart(meta2)
        
        return relation