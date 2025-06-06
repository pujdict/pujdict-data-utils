import pujpb as pb


class Pronunciation:
    def __init__(self, initial: str = None, final: str = None, tone: int = 0, sp_nasal: int = 0):
        self.initial = initial
        self.final = final
        self.tone = tone
        self.sp_nasal = sp_nasal

    def __copy__(self):
        return Pronunciation(self.initial, self.final, self.tone, self.sp_nasal)

    def __str__(self):
        return f'{self.initial}{self.final}{self.tone} {self.sp_nasal}'

    @classmethod
    def from_pb(cls, data: pb.Pronunciation):
        return cls(data.initial, data.final, data.tone, data.sp_nasal)

    def to_pb(self):
        return pb.Pronunciation(
            initial=self.initial,
            final=self.final,
            tone=self.tone,
            sp_nasal=pb.EntrySpecialNasalization.Name(self.sp_nasal),
        )


entry_index = 0


class FuzzyRule:
    description: str
    example_chars: list[str]

    def __init__(self):
        self._possible_pronunciations_map: dict[str, Pronunciation] = {}
        self._possible_pronunciations_map_reverse: dict[Pronunciation, list[Pronunciation]] = {}
        pass

    @classmethod
    def from_pb(cls, data: pb.FuzzyRule):
        rule_name: str = pb.FuzzyRule.Name(data)
        rule_class_name = rule_name.replace("FR_", "FuzzyRule_")
        rule_class = globals()[rule_class_name]
        if rule_class is None:
            return cls()
        return rule_class()

    def _fuzzy(self, result: Pronunciation):
        pass

    def fuzzy_result(self, origin: Pronunciation) -> Pronunciation:
        if origin.__str__() in self._possible_pronunciations_map:
            return self._possible_pronunciations_map[origin.__str__()]
        result = origin.__copy__()
        self._fuzzy(result)
        return result

    def cache_possible_pronunciations_map(self, possible_pronunciations: list[Pronunciation]):
        self._possible_pronunciations_map = {}
        self._possible_pronunciations_map_reverse = {}
        for pronunciation in possible_pronunciations:
            fuzzy_pronunciation = pronunciation.__copy__()
            self._fuzzy(fuzzy_pronunciation)
            self._possible_pronunciations_map[pronunciation.__str__()] = fuzzy_pronunciation
            self._possible_pronunciations_map_reverse.setdefault(fuzzy_pronunciation.__str__(), []).append(
                pronunciation)


class FuzzyRule_V_As_U(FuzzyRule):
    description = '单元音 ur 转为 u。潮阳、普宁、惠来、陆丰等地的口音。'
    example_chars = ['书', '之', '居', '鱼']

    def _fuzzy(self, result: Pronunciation):
        if result.final == 'v':
            result.final = 'u'


class FuzzyRule_R_As_O(FuzzyRule):
    description = '单元音 er 转为 o。潮汕大部分地区口音。'
    example_chars = ['坐', '罪', '短', '退']

    def _fuzzy(self, result: Pronunciation):
        if result.final == 'r':
            result.final = 'o'


class FuzzyRule_R_As_E(FuzzyRule):
    description = '单元音 er 转为 e。陆丰口音。'
    example_chars = ['坐', '罪', '短', '退']

    def _fuzzy(self, result: Pronunciation):
        if result.final == 'r':
            result.final = 'e'


class FuzzyRule_RH_As_OH(FuzzyRule):
    description = '单元音 erh 转为 oh。潮汕大部分地区口音。'
    example_chars = ['夺', '绝', '鳕', '雪']

    def _fuzzy(self, result: Pronunciation):
        if result.final == 'rh':
            result.final = 'oh'


class FuzzyRule_RM_As_IAM(FuzzyRule):
    description = 'erm 转为 iam。庄组深摄部分字音。'
    example_chars = ['森', '参', '簪']

    def _fuzzy(self, result: Pronunciation):
        if result.final == 'rm':
            result.final = 'iam'


class FuzzyRule_EU_As_IU(FuzzyRule):
    def _fuzzy(self, result: Pronunciation):
        if result.final == 'eu':
            result.final = 'iu'


class FuzzyRule_OINN_As_AINN(FuzzyRule):
    def _fuzzy(self, result: Pronunciation):
        if result.final == 'oinn':
            result.final = 'ainn'


class FuzzyRule_UOINN_As_UINN(FuzzyRule):
    def _fuzzy(self, result: Pronunciation):
        if result.final == 'uoinn':
            result.final = 'uinn'


class FuzzyRule_UOINN_As_UAINN(FuzzyRule):
    def _fuzzy(self, result: Pronunciation):
        if result.final == 'uoinn':
            result.final = 'uainn'


class FuzzyRule_OI_As_UE(FuzzyRule):
    def _fuzzy(self, result: Pronunciation):
        if result.initial in ['p', 'ph', 'm', 'b'] and result.final == 'oi':
            result.final = result.final.replace('oi', 'ue')


class FuzzyRule_OU_As_AU(FuzzyRule):
    def _fuzzy(self, result: Pronunciation):
        if result.final.startswith('ou'):
            result.final = result.final.replace('ou', 'au')


class FuzzyRule_UE_As_UEI(FuzzyRule):
    def _fuzzy(self, result: Pronunciation):
        if result.final in ['ue', 'uenn', 'ueh']:
            result.final = result.final.replace('ue', 'uei')


class FuzzyRule_VN_As_IN(FuzzyRule):
    def _fuzzy(self, result: Pronunciation):
        if result.final in ['vn', 'vt']:
            result.final = result.final.replace('v', 'i')


class FuzzyRule_IN_As_EN(FuzzyRule):
    def _fuzzy(self, result: Pronunciation):
        if result.final in ['in', 'it']:
            result.final = result.final.replace('i', 'e')


class FuzzyRule_UENG_As_ENG(FuzzyRule):
    def _fuzzy(self, result: Pronunciation):
        if result.final == 'ueng':
            if result.initial == '0':
                result.final = 'eng'
            else:
                result.final = 'uang'


class FuzzyRule_UEK_As_UAK(FuzzyRule):
    def _fuzzy(self, result: Pronunciation):
        if result.final == 'uek':
            result.final = 'uak'


class FuzzyRule_IO_As_IE(FuzzyRule):
    def _fuzzy(self, result: Pronunciation):
        if result.final in ['io', 'ionn', 'ioh']:
            result.final = result.final.replace('io', 'ie')


class FuzzyRule_IAU_As_IEU(FuzzyRule):
    def _fuzzy(self, result: Pronunciation):
        if result.final.startswith('iau'):
            result.final = result.final.replace('iau', 'ieu')


class FuzzyRule_IAU_As_IOU(FuzzyRule):
    def _fuzzy(self, result: Pronunciation):
        if result.final == 'iau':
            result.final = result.final.replace('iau', 'iou')


class FuzzyRule_IAN_As_IEN(FuzzyRule):
    def _fuzzy(self, result: Pronunciation):
        if result.final == 'ian':
            result.final = 'ien'
        elif result.final == 'iat':
            result.final = 'iet'


class FuzzyRule_UAN_As_UEN(FuzzyRule):
    def _fuzzy(self, result: Pronunciation):
        if result.final == 'uan':
            result.final = 'uen'
        elif result.final == 'uat':
            result.final = 'uet'


class FuzzyRule_IAM_As_IEM(FuzzyRule):
    def _fuzzy(self, result: Pronunciation):
        if result.final == 'iam':
            result.final = 'iem'
        elif result.final == 'iap':
            result.final = 'iep'


class FuzzyRule_N_As_L_ForMEnding(FuzzyRule):
    def _fuzzy(self, result: Pronunciation):
        if result.final.endswith('m') and result.initial == 'n':
            result.initial = 'l'


class FuzzyRule_N_As_L_ForNOrNGEnding(FuzzyRule):
    def _fuzzy(self, result: Pronunciation):
        if result.initial == 'n' and (
                (not result.final.endswith('nn') and result.final.endswith('n')) or
                result.final.endswith('ng')
        ):
            result.initial = 'l'


class FuzzyRule_L_As_N_ForMEnding(FuzzyRule):
    def _fuzzy(self, result: Pronunciation):
        if result.final.endswith('m') and result.initial == 'l':
            result.initial = 'n'


class FuzzyRule_MU_As_BU_ForNasalEnding(FuzzyRule):
    def _fuzzy(self, result: Pronunciation):
        if result.initial == 'm' and result.final.startswith('u') and (
                (not result.final.endswith('nn') and result.final.endswith('n')) or
                result.final.endswith('ng')
        ):
            result.initial = 'b'


class FuzzyRule_BU_As_MU_ForNasalEnding(FuzzyRule):
    def _fuzzy(self, result: Pronunciation):
        if result.initial == 'b' and result.final.startswith('u') and (
                (not result.final.endswith('nn') and result.final.endswith('n')) or
                result.final.endswith('ng')
        ):
            result.initial = 'm'


class FuzzyRule_Labiodentalized(FuzzyRule):
    def _fuzzy(self, result: Pronunciation):
        if result.final.startswith('u'):
            if result.initial == 'h':
                result.initial = 'f'
            elif result.initial in ['p', 'ph']:
                result.initial += 'f'
            elif result.initial in ['m', 'b']:
                result.initial += 'v'


class FuzzyRule_N_As_NG(FuzzyRule):
    def _fuzzy(self, result: Pronunciation):
        if result.final.endswith('n') and not result.final.endswith('nn'):
            result.final = result.final.replace('n', 'ng')
        elif result.final.endswith('t'):
            result.final = result.final.replace('t', 'k')


class FuzzyRule_M_As_NG(FuzzyRule):
    def _fuzzy(self, result: Pronunciation):
        if result.final.endswith('m'):
            result.final = result.final.replace('m', 'ng')
        elif result.final.endswith('p'):
            result.final = result.final.replace('p', 'k')


class FuzzyRule_ENG_As_EN(FuzzyRule):
    def _fuzzy(self, result: Pronunciation):
        if result.final == 'eng':
            result.final = 'en'
        elif result.final == 'ek':
            result.final = 'et'


class FuzzyRule_NG_As_UNG(FuzzyRule):
    def _fuzzy(self, result: Pronunciation):
        if result.initial in ['p', 'ph', 'm', 'b'] and result.final == 'ng':
            result.final = 'ung'


class FuzzyRule_NG_As_VNG(FuzzyRule):
    def _fuzzy(self, result: Pronunciation):
        if result.final == 'ng' and result.initial not in ['h', '0']:
            result.final = 'vng'


class FuzzyRule_IONG_As_ONG(FuzzyRule):
    def _fuzzy(self, result: Pronunciation):
        if result.initial in ['t', 'th', 'n', 'l', 'ts', 'tsh', 's', 'j'] and result.final == 'iong':
            result.final = 'ong'
        elif result.initial in ['t', 'n', 'l', 'ts', 'tsh', 's', 'j'] and result.final == 'iok':
            result.final = 'ok'


class FuzzyRule_NGU_As_U(FuzzyRule):
    def _fuzzy(self, result: Pronunciation):
        if result.initial == 'ng' and result.final == 'u':
            result.initial = '0'


class FuzzyRule_RemoveApostrophe(FuzzyRule):
    def _fuzzy(self, result: Pronunciation):
        result.initial = result.initial.replace("'", '')
        result.final = result.final.replace("'", '')


class Accent(FuzzyRule):
    id: str
    area: str
    subarea: str
    rules: list[FuzzyRule]

    def _fuzzy(self, result: Pronunciation):
        for rule in self.rules:
            rule._fuzzy(result)

    @classmethod
    def from_pb(cls, data: pb.Accent):
        result = Accent()
        result.id = data.id
        result.area = data.area
        result.subarea = data.subarea
        result.rules = [FuzzyRule.from_pb(rule) for rule in data.rules]
        return result


class Accent_Dummy(Accent):
    id = 'Dummy'
    area = ''
    subarea = ''
    rules = []
