<script>
    import { goto } from '$app/navigation'

    import Modal from '$lib/components/Modal.svelte'

    let showParentsModal = $state(false)
</script>

<style>
    .content {
        height: 100vh;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }

    .exam-results-input {
        height: 150px;
        width: 100%;
        font-family: monospace;
        resize: none;
    }
</style>

{#if showParentsModal}
    <Modal onclose={() => showParentsModal = false}>
        {#snippet title()}
            Show Exam Results to Timmy's Parents
        {/snippet}

        {#snippet body()}
            <p>
                Are you ready to show Timmy's parents the exam results?
                They will be really mad if Timmy didn't pass!
            </p>

            <form action="/parents" method="POST" id="resultsForm">
                <label class="w-100">
                    Exam Results
                    <textarea
                        class="form-control exam-results-input"
                        name="resultsRef"
                    ></textarea>
                </label>
            </form>
        {/snippet}

        {#snippet footer()}
            <button class="btn btn-primary" form="resultsForm">
                Submit
            </button>
        {/snippet}
    </Modal>
{/if}

<div class="content">
    <h1 class="mb-3">Exam System</h1>

    <button
        class="btn btn-primary mb-3"
        onclick={() => goto('/exam')}
    >
        Attempt the Exam
    </button>

    <button
        class="btn btn-secondary"
        onclick={() => showParentsModal = true}
    >
        Show the results to Timmy's parents
    </button>
</div>
