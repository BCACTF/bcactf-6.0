#!/usr/bin/env -S deno run --allow-net

const url = prompt('URL:')

const selections = Array(25).fill(0)

const { examRef } = await (await fetch(url + '/api/exam/begin', {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ studentName: 'Timmy Bobbins' })
})).json()

while (true) {
    try {
        const { passed, resultsRef } = await (await fetch(url + '/api/exam/submit', {
            method: 'POST',
            headers: { 'content-type': 'application/json' },
            body: JSON.stringify({ examRef, selections })
        })).json()

        console.log(resultsRef)

        if (passed) {
            console.log('Done.')
            break
        }

        const wrong = prompt('Wrong questions (space-delimited):')
            .split(' ')
            .map(Number)

        for (const questionNumber of wrong) {
            selections[questionNumber - 1]++
        }
    } catch {
        continue
    }
}
