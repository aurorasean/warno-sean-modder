
import type { Deck } from "./types";
const processUnits = (deck: Deck) => {
    deck.deckPackList = [];
    deck.deckPackList.length = 0;
    let currentIndex = 0;
    deck.groups.forEach((group) => {
        group.SmartGroupList.forEach((smartGroup) => {
            smartGroup.members.forEach((member) => {
                member.index = currentIndex;
                for (let i = 0; i < member.numberofUnits; i++) {
                    deck.deckPackList.push(member.unitName);
                }
                currentIndex += member.numberofUnits;
            });
        });
    });
    return deck;
};

export const MakeMaxDeck = (deckin: Deck) => {
    deckin.groups.forEach((group) => {
        group.SmartGroupList.forEach((smartGroup) => {
            smartGroup.members.forEach((member) => {
                member.numberofUnits = 400;
            });
        });
    });
    deckin = processUnits(deckin);
    return fetch("http://localhost:5000/api/mod-decks", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(deckin),
    })
        .then((response) => response.json())
        .then((data) => {
            console.log("Deck saved:", data);
        })
        .catch((error) => {
            console.error("Error saving deck:", error);
        });
}