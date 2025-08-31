class CharacterCost:
    _constelations_count = 7
    _cost_arr = []

    def __init__(self):
        self._cost_arr = [0 for _ in range(self._constelations_count)]

    def set_constelation_value_by_index(self, constelation_idx: int, cost_value: int):
        assert 0 <= constelation_idx < self._constelations_count
        self._cost_arr[constelation_idx] = cost_value

    def get_constelation_value_by_index(self, constelation_idx: int) -> int:
        assert 0 <= constelation_idx < self._constelations_count
        return self._cost_arr[constelation_idx]
    
    @staticmethod
    def get_constelations_count() -> int:
        return CharacterCost._constelations_count

    @property
    def c0_cost(self) -> int:
        return self.get_constelation_value_by_index(0)
    
    @property
    def c1_cost(self) -> int:
        return self.get_constelation_value_by_index(1)
    
    @property
    def c2_cost(self) -> int:
        return self.get_constelation_value_by_index(2)
    
    @property
    def c3_cost(self) -> int:
        return self.get_constelation_value_by_index(3)
    
    @property
    def c4_cost(self) -> int:
        return self.get_constelation_value_by_index(4)
    
    @property
    def c5_cost(self) -> int:
        return self.get_constelation_value_by_index(5)
    
    @property
    def c6_cost(self) -> int:
        return self.get_constelation_value_by_index(6)
    
    def __str__(self) -> str:
        return f'C0: {self.c0_cost}, \
        C1: {self.c1_cost}, \
        C2: {self.c2_cost}, \
        C3: {self.c3_cost}, \
        C4: {self.c4_cost}, \
        C5: {self.c5_cost}, \
        C6: {self.c6_cost}'


characters_list = [
    'Albedo',
    'Alhaitham',
    'Arlecchino', # Mhmm <3
    'Ayaka',
    'Ayato',
    'Baizhu',
    'Chasca',
    'Chevreuse',
    'Chiori',
    'Citlali',
    'Clorinde',
    'Cyno',
    'Dehya',
    'Diluc',
    'Emilie',
    'Escoffier',
    'Eula',
    'Faruzan',
    'Furina',
    'Gaming',
    'Ganyu',
    'Hu Tao',
    'Iansan',
    'Ineffa',
    'Itto',
    'Jean',
    'Kazuha',
    'Keqing',
    'Kinich',
    'Klee',
    'Kokomi',
    'Lyney',
    'Mavuika',
    'Mizuki',
    'Mona',
    'Mualani',
    'Nahida',
    'Navia',
    'Neuvillette',
    'Nilou',
    'Ororon',
    'Raiden',
    'Shenhe',
    'Sigewinne',
    'Skirk',
    'Tartaglia',
    'Tighnari',
    'Varesa',
    'Venti',
    'Wanderer',
    'Wriothesley',
    'Xianyun',
    'Xiao',
    'Xilonen',
    'Yae Miko',
    'Yelan',
    'Yoimiya',
    'Zhongli'
]
