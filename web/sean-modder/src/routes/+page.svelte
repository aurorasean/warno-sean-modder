<script lang="ts">
    import { onMount } from "svelte";
    import Paper, { Title, Subtitle, Content } from "@smui/paper";
    import Textfield from "@smui/textfield";
    import IconButton, { Icon } from "@smui/icon-button";
    import type { Deck } from "$lib/types";
    import UnModded from "$lib/UnModded.svelte";
    import Chip, { Set, LeadingIcon, TrailingIcon, Text } from "@smui/chips";
    import Modded from "$lib/Modded.svelte";
    import Card from "@smui/card";
    import ModCreator from "$lib/ModCreator.svelte";
    import Button, { Label } from "@smui/button";
    import { MakeMaxDeck } from "$lib/utilts";
    let filterValue = '{"namespace": {"$regex": ".*"}}';
    let invalidFitler = false;
    let statusBackend = "";

    const isEnter = (e: any) => {
        if (e.key === "Enter") {
            onPageChange();
        }
    };

    const handleValidFilter = (event: any) => {
        try {
            JSON.parse(event.target.value);
            filterValue = event.target.value;
            invalidFitler = false;
        } catch (error) {
            invalidFitler = true;
            console.error("Invalid JSON filter:", error);
        }
    };

    const getStatus = async () => {
        const response = await fetch(`http://localhost:5000/api/status`);
        const { message: status } = await response.json();
        statusBackend = status;
        if (status === "No Mods") {
            // show the mod add only
        }
    };
    onMount(async () => {
        try {
            await getStatus();
        } catch (error) {
            console.error("Failed to fetch decks:", error);
        }
    });
    let unmoddedComponent: UnModded;
    let moddedComponent: Modded;
    let generatorComponent: ModCreator;
    const onPageChange = async () => {
        await unmoddedComponent.onPageChange();
        await moddedComponent.onPageChange();
    };

    const updated = (ee: any) => {
        console.log({ ee });
        if (ee.text === "unmodded updated") {
            unmoddedComponent.onPageChange();
        } else {
            moddedComponent.onPageChange();
        }
        generatorComponent.getDataCall();
        // onPageChange();
    };
    let disableMax = false;
    const handleMaxAll = async () => {
        disableMax = true;
        // get all data from the db
        const response = await fetch(
            `http://localhost:5000/api/decks?filter=${filterValue}&limit=1000&skip=0`,
        );
        const { data } = await response.json();
        const decks = data as Deck[];
        // for each deck, max all
        for await (const deck of decks) {
            await MakeMaxDeck(deck);
        }
        disableMax = false;
    };
</script>

<div class="paper-container">
    <Card>
        <h1>Sean Modder</h1>
        <!-- <Set chips={["one"]} let:chip>
            <Chip {chip}>
                {statusBackend}
            </Chip>
        </Set> -->
        <Content>
            <h2>Decks</h2>
            <div class="row2">
                <Textfield
                    invalid={invalidFitler}
                    bind:value={filterValue}
                    on:change={handleValidFilter}
                    on:keyup={isEnter}
                    style="width: 100%;"
                    helperLine$style="width: 100%;"
                    label="Filter"
                >
                    <Icon class="material-icons" slot="leadingIcon">filter</Icon
                    >
                </Textfield>
                <IconButton
                    class="material-icons"
                    on:click={() => {
                        onPageChange();
                    }}
                    >search
                </IconButton>
            </div>
            <br />
            <Paper>
                <UnModded
                    bind:this={unmoddedComponent}
                    on:updated={updated}
                    bind:filterValue
                />
            </Paper>
            <br />
            <Paper>
                <h3>Modded decks</h3>
                <Subtitle>These are decks you have modified</Subtitle>
                <Modded
                    bind:this={moddedComponent}
                    on:updated={updated}
                    bind:filterValue
                />
            </Paper>
            <br />
            <Paper>
                <h3>Generate</h3>
                <ModCreator bind:this={generatorComponent} />
            </Paper>
            <br />
            <Paper>
                <Button
                    disabled={disableMax}
                    on:click={() => {
                        handleMaxAll();
                    }}
                >
                    <Label>Max Everything in filter</Label>
                </Button>
            </Paper>
        </Content>
    </Card>
</div>

<style>
    .paper-container {
        display: flex;
        justify-content: center;
        margin-top: 2rem;
        margin: auto;
        min-width: 90vw;
        max-width: 90vw;
    }
    .row2 {
        display: flex;
    }
</style>
