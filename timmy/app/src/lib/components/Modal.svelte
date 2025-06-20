<script>
    import { onMount } from 'svelte'

    import { quintOut } from 'svelte/easing'
    import { fade, fly } from 'svelte/transition'

    import { createFocusTrap } from 'focus-trap'

    let {
        lg = false,
        fullscreen = false,
        showClose = true,
        animateOut = true,
        title,
        body,
        footer,
        onclose = () => {}
    } = $props()

    let modal

    onMount(() => {
        const trap = createFocusTrap(modal).activate()
        return () => trap.deactivate()
    })
</script>

<svelte:head>
    <style>
        body {
            overflow: hidden;
        }
    </style>
</svelte:head>

<div
    class="modal d-block"
    class:modal-lg={lg}
    bind:this={modal}
    in:fly|global={{ y: -50, duration: 300 }}
    out:fly|global={{ y: -50, duration: 300, easing: quintOut }}
>
    <div class="modal-dialog modal-dialog-centered" class:modal-fullscreen={fullscreen}>
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title text-wrap text-break">
                    {@render title()}
                </h5>

                {#if showClose}
                    <!-- svelte-ignore a11y_consider_explicit_label -->
                    <button class="btn-close" onclick={onclose}></button>
                {/if}
            </div>

            <div class="modal-body">
                {@render body()}
            </div>

            {#if footer}
                <div class="modal-footer py-2">
                    {@render footer()}
                </div>
            {/if}
        </div>
    </div>
</div>

<div
    class="modal-backdrop show"
    in:fade={{ duration: 150 }}
    out:fade={{ duration: animateOut ? 150 : 0 }}
></div>
