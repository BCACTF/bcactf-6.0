import { randomInt } from 'crypto'

import { shuffle } from '$lib/shuffle.js'

const kDegree = 3

const superscriptPowers = ['²', '³', '⁴', '⁵', '⁶', '⁷', '⁸', '⁹']

const generateDerivativeQuestion = () => {
    const terms = []

    for (let i = kDegree; i >= 0; i--) {
        let coefficient = randomInt(2, 128)

        if (randomInt(0, 2)) {
            coefficient *= -1
        }

        terms.push({
            coefficient,
            power: i
        })
    }

    let correctAnswer

    const answerChoices = new Set()

    while (answerChoices.size < 5) {
        const point = randomInt(16, 512)

        let slope = 0

        for (const term of terms) {
            slope += (term.coefficient * term.power) * (point ** (term.power - 1))
        }

        if (!answerChoices.size) {
            correctAnswer = [point, slope]
        }

        answerChoices.add(slope)
    }

    const representedTerms = []

    for (const term of terms) {
        let representation = `${term.coefficient}`

        if (term.power > 1) {
            representation += `x${superscriptPowers[term.power -    2]}`
        } else if (term.power === 1) {
            representation += 'x'
        }

        representedTerms.push(representation)
    }

    const expr = representedTerms.join(' + ').replaceAll('+ -', '- ')

    const choices = shuffle([...answerChoices])

    return {
        problemStatement: `Find the slope of the curve ${expr} at the ` +
            `point x=${correctAnswer[0]}.`,
        choices,
        answer: choices.indexOf(correctAnswer[1])
    }
}

export { generateDerivativeQuestion }
