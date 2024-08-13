<script lang="ts">
    export let deck: Deck;
    import Slider from "@smui/slider";
    import FormField from "@smui/form-field";
    import Dialog, {
        Title,
        Content,
        Actions,
        InitialFocus,
    } from "@smui/dialog";
    import Button, { Label } from "@smui/button";

    import { createEventDispatcher } from "svelte";
    export let isDeletable = false;
    const dispatch = createEventDispatcher();

    const updated = () => {
        dispatch("updated", {
            text: "updated",
        });
    };

    let open = false;
    import Card from "@smui/card";
    import IconButton, { Icon } from "@smui/icon-button";
    import type { Deck } from "./types";
    import Paper from "@smui/paper";

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

    const handleMax = (deckin: Deck) =>{
        deckin.groups.forEach((group) => {
            group.SmartGroupList.forEach((smartGroup) => {
                smartGroup.members.forEach((member) => {
                    member.numberofUnits = 400;
                });
            });
        });
        deckin = processUnits(deckin);
        fetch("http://localhost:5000/api/mod-decks", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(deckin),
        })
            .then((response) => response.json())
            .then((data) => {
                console.log("Deck saved:", data);
                updated();
            })
            .catch((error) => {
                console.error("Error saving deck:", error);
            });
    }
    const handleSliderChange = (
        deckName: string,
        groupName: string,
        unitName: string,
        amount: number,
    ) => {
        // send to backend to store the entire deck as changed
        console.log(deckName, groupName, unitName, amount);
        deck = processUnits(deck);
        console.log("Deck:", deck);
        fetch("http://localhost:5000/api/mod-decks", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(deck),
        })
            .then((response) => response.json())
            .then((data) => {
                console.log("Deck saved:", data);
                updated();
            })
            .catch((error) => {
                console.error("Error saving deck:", error);
            });
        // save to db the entire deck
    };
    const handleDelete = (deckName: string) => {
        // send to backend to delete the deck
        console.log(deckName);
        fetch(`http://localhost:5000/api/delete-mod-decks`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ namespace: deckName }),
        })
            .then((response) => response.json())
            .then((data) => {
                console.log("Deck deleted:", data);
                updated();
            })
            .catch((error) => {
                console.error("Error deleting deck:", error);
            });
    };
</script>

<div class="card-deck-limit">
    <Card>
        <Content>
            {deck.namespace.replace(/_/g, " ").replace("Descriptor", "")}
        </Content>
        <Actions>
            {#if isDeletable}
                <IconButton
                    class="material-icons"
                    on:click={() => handleDelete(deck.namespace)}
                >
                    delete
                </IconButton>
            {/if}
            <IconButton class="material-icons" on:click={() => (open = true)}>
                edit
            </IconButton>
        </Actions>
    </Card>
</div>
<Dialog bind:open surface$style="width: 850px; max-width: calc(100vw - 32px);">
    <Title id="default-focus-title"
        >Edit {deck.namespace
            .replace(/_/g, " ")
            .replace("Descriptor", "")}</Title
    >

    <Content id="default-focus-content">
        {#each deck.groups as group}
            <!-- content here -->
            <Paper variant="outlined">
                <Title
                    >{group.namespace
                        .replace("Descriptor_CombatGroup_pion_", "")
                        .replace(/_/g, " ")}</Title
                >
                <Content>
                    <h3>Smart Groups</h3>
                    {#each group.SmartGroupList as smartGroup}
                        <Card>
                            <Title>{smartGroup.name}</Title>
                            {#each smartGroup.members as member}
                                <Card>
                                    <Title
                                        >{member.unitName
                                            .replace(
                                                "Descriptor_StrategicPack_",
                                                "",
                                            )
                                            .replace(/_/g, " ")}</Title
                                    >
                                    <Content>
                                        <FormField
                                            style="display: flex; flex-direction: column-reverse;"
                                        >
                                            <Slider
                                                on:SMUISlider:change={() => {
                                                    // do something with the value here
                                                    handleSliderChange(
                                                        deck.namespace,
                                                        group.namespace,
                                                        member.unitName,
                                                        member.numberofUnits,
                                                    );
                                                }}
                                                min={1}
                                                max={400}
                                                bind:value={member.numberofUnits}
                                                style="width: 100%;"
                                            />
                                            <span slot="label"
                                                >{member.numberofUnits}</span
                                            >
                                        </FormField>
                                    </Content>
                                </Card>
                            {/each}
                        </Card>
                    {/each}
                </Content>
            </Paper>
        {/each}
    </Content>
    <Actions>
        <Button use={[InitialFocus]} on:click={() => {handleMax(deck)}}>
            <Label>MAX</Label>
        </Button>
        <Button defaultAction use={[InitialFocus]} on:click={() => {}}>
            <Label>Close</Label>
        </Button>
    </Actions>
</Dialog>

<style>
    .card-deck-limit {
        width: 27rem;
    }
</style>
