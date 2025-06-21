<script>
    import Modal from '$lib/components/Modal.svelte'

    let { examResults, onexit } = $props()
</script>

<style>
    .results {
        width: 100%;
        height: 150px;
        font-family: monospace;
        resize: none;
    }

    .pass-text {
        color: #90ee90;
    }

    .fail-text {
        color: #ff2c2c;
    }
</style>

<Modal showClose={false}>
    {#snippet title()}
        Exam Results
    {/snippet}

    {#snippet body()}
        <h2 class="text-center mb-1">Your score:</h2>

        <h3
            class="text-center"
            class:pass-text={examResults.passed}
            class:fail-text={!examResults.passed}
        >{examResults.score}</h3>

        <p class="text-center">
            {#if examResults.passed}
                YOU PASSED!!!
            {:else}
                YOU FAILED!!!
            {/if}
        </p>

        <p class="mb-2">
            Send your results to your parents so they can check
            your score:
        </p>

        <textarea
            class="results form-control"
            readonly
        >{examResults.resultsRef}</textarea>
    {/snippet}

    {#snippet footer()}
        <button
            class="btn btn-primary"
            onclick={onexit}
        >Exit Exam</button>
    {/snippet}
</Modal>
