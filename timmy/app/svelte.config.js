import adapter from '@sveltejs/adapter-node'

const config = {
    kit: {
        adapter: adapter(),
        csrf: {
            checkOrigin: false
        }
    },
    compilerOptions: { runes: true }
}

export default config
