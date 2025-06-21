import adapter from '@sveltejs/adapter-static'

const config = {
    kit: { adapter: adapter() },
    compilerOptions: { runes: true }
}

export default config
