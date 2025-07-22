import enum


class SexeEnum(enum.Enum):
    H = 'Homme'
    F = 'Femme'
    A = 'Autre'

class SituationFamilialeEnum(enum.Enum):
    marié = 'marié(e)'
    célibataire = 'célibataire'
    veuf = 'veuf(ve)'
    divorcé = 'divorcé(e)'
    pacsé = 'pacsé(e)'
