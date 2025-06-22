<script>
    import { goto } from '$app/navigation'

    import Modal from '$lib/components/Modal.svelte'

    import ResultsModal from './ResultsModal.svelte'

    let studentName = $state('')

    let loading = $state(false)
    let errorMessage = $state(null)

    let exam = $state(null)
    let examResults = $state(null)

    let selections = $state(Array(25).fill(null))

    const letters = ['a.', 'b.', 'c.', 'd.', 'e.']

    const begin = async () => {
        errorMessage = null
        loading = true

        try {
            const res = await fetch('/api/exam/begin', {
                method: 'POST',
                headers: { 'content-type': 'application/json' },
                body: JSON.stringify({ studentName })
            })

            const body = await res.json()

            if (res.status < 200 || res.status > 299) {
                errorMessage = body.error
                console.log(body.error)
                return
            }

            exam = body
        } catch (error) {
            errorMessage = error.message
        } finally {
            loading = false
        }
    }

    const submit = async () => {
        if (selections.some(selection => selection === null)) {
            errorMessage = 'Please answer all questions.'
            return
        }

        errorMessage = null
        loading = true

        try {
            const res = await fetch('/api/exam/submit', {
                method: 'POST',
                headers: { 'content-type': 'application/json' },
                body: JSON.stringify({
                    examRef: exam.examRef,
                    selections: $state.snapshot(selections)
                })
            })

            const body = await res.json()

            if (res.status < 200 || res.status > 299) {
                errorMessage = body.error
                return
            }

            examResults = body
        } catch (error) {
            errorMessage = error.message
        } finally {
            loading = false
        }
    }
</script>

<svelte:head>
    {#if loading}
        <style>
            body {
                overflow: hidden;
            }
        </style>
    {/if}
</svelte:head>

<style>
    .loading {
        position: fixed;
        top: 0;
        left: 0;

        height: 100vh;
        width: 100vw;

        background-color: #00000080;

        display: flex;
        align-items: center;
        justify-content: center;
    }

    .submission-spinner {
        height: 75px;
        width: 75px;
    }

    .name-inputs {
        max-width: 400px;
    }
</style>

<div class="m-3">
    <h1>Exam</h1>

    {#if errorMessage}
        {#if exam}
            <Modal onclose={() => errorMessage = null}>
                {#snippet title()}
                    Error
                {/snippet}

                {#snippet body()}
                    <div class="alert alert-danger">
                        {errorMessage}
                    </div>
                {/snippet}

                {#snippet footer()}
                    <button
                        class="btn btn-primary"
                        onclick={() => errorMessage = null}
                    >OK</button>
                {/snippet}
            </Modal>
        {:else}
            <div class="alert alert-danger">
                {errorMessage}
            </div>
        {/if}
    {/if}

    {#if exam}
        {#if loading}
            <div class="loading">
                <div class="spinner-border submission-spinner"></div>
            </div>
        {/if}

        <h5 class="mb-3">Student: {exam.studentName}</h5>

        <p class="mb-1">
            You must score <b>25/25</b> to pass this exam.
            You have 2 minutes. Good luck!
        </p>

        <p>
            Select the best answer for each question.
            Each question has a single best answer.
        </p>

        <ol>
            {#each exam.questions as question, questionIndex}
                <li class="mb-3">
                    <p class="mb-2">{question.problemStatement}</p>

                    {#each question.choices as choice, choiceIndex}
                        <div class="form-check">
                            <label class="form-check-label">
                                {letters[choiceIndex]} {choice}

                                <input
                                    type="radio"
                                    class="form-check-input"
                                    name="question{questionIndex}"
                                    value={choiceIndex}
                                    disabled={loading}
                                    bind:group={selections[questionIndex]}
                                />
                            </label>
                        </div>
                    {/each}
                </li>
            {/each}
        </ol>

        <button
            class="btn btn-primary mt-1"
            disabled={loading}
            onclick={submit}
        >Submit Exam</button>
    {:else}
        <p class="mb-1">Are you ready to start the exam?</p>

        <p>
            You have infinite attempts, but our system will give you
            unique questions each time!
        </p>

        <div class="name-inputs">
            <label class="d-block mb-1">
                Student Name
                <input
                    type="text"
                    class="form-control mb-4"
                    disabled={loading}
                    bind:value={studentName}
                />
            </label>
        </div>

        <button
            class="btn btn-primary"
            disabled={loading}
            onclick={begin}
        >Begin Exam</button>
    {/if}
</div>

{#if examResults}
    <ResultsModal {examResults} onexit={() => goto('/')} />
{/if}
