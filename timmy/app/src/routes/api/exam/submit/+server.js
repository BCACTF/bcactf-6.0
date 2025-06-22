import { json } from '@sveltejs/kit'

import { setTimeout } from 'timers/promises'

import Joi from 'joi'

import { decrypt, encrypt } from '$lib/encryption.js'

const kResultsExpiration = 5 * 60 * 1000

const blacklist = new Set()

export const POST = async ({ request }) => {
    const body = await request.json()

    const validation = Joi.object({
        examRef: Joi.string(),
        selections: Joi.array().length(25).items(Joi.valid(0, 1, 2, 3, 4))
    }).required().validate(body)

    if (validation.error) {
        return json({ error: validation.error.message }, { status: 422 })
    }

    let examDetails

    try {
        examDetails = await decrypt(body.examRef, 'examData')
    } catch (error) {
        return json({
            error: '"examRef" is not part of this chall\'s solution!'
        }, { status: 422 })
    }

    if (examDetails.endTime < new Date()) {
        return json({
            error: 'It was a 2-minute exam! You took too long...'
        }, { status: 403 })
    }

    if (blacklist.has(examDetails.examId)) {
        return json({
            error: 'Your exam is already being graded.'
        }, { status: 409 })
    }

    blacklist.add(examDetails.examId)

    await setTimeout(5_000)

    blacklist.delete(examDetails.examId)

    const results = Array(25).fill('0')

    for (let i = 0; i < 25; i++) {
        if (body.selections[i] === examDetails.answers[i]) {
            results[i] = '1'
        }
    }

    const correct = results.filter(status => status === '1').length

    return json({
        score: `${((correct / 25) * 100).toFixed(1)}%`,
        passed: correct === 25,
        resultsRef: await encrypt({
            studentName: examDetails.studentName,
            expires: new Date(Date.now() + kResultsExpiration).getTime(),
            results: results.join('')
        }, 'examResults')
    })
}
