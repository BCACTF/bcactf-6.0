import { randomInt } from 'crypto'

const shuffle = array => {
    for (let i = array.length - 1; i > 0; i--) {
        const j = randomInt(0, i + 1)
        { [array[i], array[j]] = [array[j], array[i]] }
    }

    return array
}

export { shuffle }
