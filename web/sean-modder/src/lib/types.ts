export interface Deck {
    _id: Id
    namespace: string
    deckDivision: string
    deckCombatGroupList: string[]
    divisionNational: string
    deckPackList: string[]
    groups: Group[]
}

export interface Id {
    $oid: string
}

export interface Group {
    namespace: string
    SmartGroupList: SmartGroupList[]
}

export interface SmartGroupList {
    name: string
    members: Member[]
}

export interface Member {
    unitName: string
    index?: number;
    numberofUnits: number
}
