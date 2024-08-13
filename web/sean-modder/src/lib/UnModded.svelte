<script lang="ts">
    import { onMount } from "svelte";
    import Select, { Option } from "@smui/select";
    import DataTable, { Pagination } from "@smui/data-table";
    import { Label } from "@smui/button";
    import IconButton from "@smui/icon-button";
    import type { Deck } from "$lib/types";
    import DeckCard from "$lib/DeckCard.svelte";

    let decks: Deck[] = [];
    export let filterValue = '{"namespace": {"$regex": ".*"}}';
    let rowsPerPage = 10;
    let currentPage = 0;
    let total = 0;
    $: start = currentPage * rowsPerPage;
    $: end = Math.min(start + rowsPerPage, total);
    $: lastPage = Math.max(Math.ceil(total / rowsPerPage) - 1, 0);

    $: if (currentPage > lastPage) {
        currentPage = lastPage;
    }

    import { createEventDispatcher } from "svelte";

    const dispatch = createEventDispatcher();

    const updated = () => {
        dispatch("updated", {
            text: "unmodded updated",
        });
    };

    export const onPageChange = async () => {
        await getData();
    };
    const getData = async () => {
        const response = await fetch(
            `http://localhost:5000/api/decks?filter=${filterValue}&limit=${rowsPerPage}&skip=${currentPage * rowsPerPage}`,
        );
        const { data, total: inTotal } = await response.json();
        decks = data as Deck[];
        total = inTotal;
    };

    onMount(async () => {
        try {
            await getData();
        } catch (error) {
            console.error("Failed to fetch decks:", error);
        }
    });
</script>

<DataTable table$aria-label="Todo list" style="width: 100%;">
    <div class="card-container">
        {#each decks as deck}
            <DeckCard {deck} on:updated={updated} />
        {/each}
    </div>
    <div></div>

    <Pagination slot="paginate">
        <svelte:fragment slot="rowsPerPage">
            <Label>Rows Per Page</Label>
            <Select
                variant="outlined"
                bind:value={rowsPerPage}
                on:change={() => onPageChange()}
                noLabel
            >
                <Option value={10}>10</Option>
                <Option value={25}>25</Option>
                <Option value={100}>100</Option>
                <Option value={200}>200</Option>
            </Select>
        </svelte:fragment>
        <svelte:fragment slot="total">
            {start + 1}-{end} of {total}
        </svelte:fragment>

        <IconButton
            class="material-icons"
            action="first-page"
            title="First page"
            on:click={() => (currentPage = 0) && onPageChange()}
            disabled={currentPage === 0}>first_page</IconButton
        >
        <IconButton
            class="material-icons"
            action="prev-page"
            title="Prev page"
            on:click={() => currentPage-- && onPageChange()}
            disabled={currentPage === 0}>chevron_left</IconButton
        >
        <IconButton
            class="material-icons"
            action="next-page"
            title="Next page"
            on:click={() => currentPage++ && onPageChange()}
            disabled={currentPage === lastPage}>chevron_right</IconButton
        >
        <IconButton
            class="material-icons"
            action="last-page"
            title="Last page"
            on:click={() => (currentPage = lastPage) && onPageChange()}
            disabled={currentPage === lastPage}>last_page</IconButton
        >
    </Pagination>
</DataTable>

<style>
    .card-container {
        display: flex;
        flex-wrap: wrap;
        gap: 1rem;
    }
</style>
