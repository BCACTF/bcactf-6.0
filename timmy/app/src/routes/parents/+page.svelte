<script>
    import { goto } from '$app/navigation'

    let { form } = $props()

    const lines = {
        fail: [
            'TIMOTHY ROBIN BOBBINS, WE\'RE SO DISAPPOINTED IN YOU!!!',
            'You FAILED your exam!',
            'You\'re grounded for LIFE!!!'
        ],
        expired: [
            'Timmy, your teacher won\'t let us verify your results.',
            'Exam results are only valid for 5 minutes after submission...'
        ],
        unknownStudent: [
            'You\'re not Timmy!!',
            'Our child is Timmy Bobbins. We don\'t you who you are!'
        ],
        pass: [
            'Good job, Timmy!',
            'You passed the exam.'
        ],
        malformed: [
            'Timmy, what is this?',
            'Your exam results string is invalid.'
        ]
    }
</script>

<style>
    .angry-parent {
        height: 350px;
    }
</style>

<div class="m-5">
    <div class="text-center mb-5">
        {#each lines[form.status] as line, index}
            <svelte:element this={`h${index + 1}`}>{line}</svelte:element>
        {/each}

        {#if form.status === 'pass'}
            <h3>{form.flag}</h3>
        {/if}
    </div>

    {#if form.status !== 'passed'}
        <!-- svelte-ignore a11y_missing_attribute -->
        <div class="text-center">
            <img src="/angryman.png" class="angry-parent me-5" />

            {#if form.angryWoman}
                <img src={form.angryWoman} class="angry-parent" />
            {:else}
                <img src="/angrywoman.png" class="angry-parent" />
            {/if}
        </div>
    {/if}
</div>
