<script lang="ts">
    import { onMount } from "svelte";
    import Button, { Label } from "@smui/button";
    import Paper from "@smui/paper";
    let isBusy = false;
    let total = 0;
    const getData = async () => {
        const response = await fetch(
            `http://localhost:5000/api/modded-decks?limit=10`,
        );
        const { data, total: inTotal } = await response.json();
        total = inTotal;
    };

    const makeNdfChanges = () => {
        isBusy = true;
        fetch("http://localhost:5000/api/make-ndf", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({}),
        })
            .then((response) => response.json())
            .then((data) => {
                console.log("Deck saved:", data);
                isBusy = false;
            })
            .catch((error) => {
                isBusy = false;
                console.error("Error saving deck:", error);
            });
    };
    onMount(async () => {
        try {
            await getData();
        } catch (error) {
            console.error("Failed to fetch decks:", error);
        }
    });
    export const getDataCall = async () => {
        getData();
    };
</script>

<Paper>
    <Button
        disabled={total === 0 || isBusy}
        variant="raised"
        on:click={() => {
            makeNdfChanges();
        }}
    >
        <Label>Make NDF files</Label>
    </Button>
</Paper>
