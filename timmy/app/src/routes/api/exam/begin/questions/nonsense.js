import { readFileSync } from 'fs'
import { randomInt } from 'crypto'

let nouns
let articles

{
    const lines = readFileSync('private/nouns.txt', 'utf-8').split('\n')
    nouns = lines.slice(0, -1)
    articles = lines.at(-1).split(' ')
}

const a = word => `${articles[nouns.indexOf(word)]} ${word}`

const generateWords = (length, result = []) => {
    if (result.length >= length) {
        return result
    }

    const selection = nouns[randomInt(0, nouns.length)]

    if (result.includes(selection)) {
        return generateWords(length, result)
    }

    return generateWords(length, [...result, selection])
}

const generateNonsenseQuestion = () => {
    const words = generateWords(10).map((w, i) => i < 5 ? a(w) : w)

    return {
        problemStatement: `What do you get when you mix ${words[0]}, ${words[1]}, `
            + `${words[2]}, ${words[3]}, and ${words[4]}?`,
        choices: words.slice(5),
        answer: randomInt(0, 5)
    }
}

export { generateNonsenseQuestion }
