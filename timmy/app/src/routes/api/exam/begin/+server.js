import { json } from '@sveltejs/kit'

import { randomUUID } from 'crypto'

import Joi from 'joi'

import { shuffle } from '$lib/shuffle.js'
import { encrypt, decrypt } from '$lib/encryption.js'

import { generateNonsenseQuestion } from './questions/nonsense.js'
import { generateDerivativeQuestion } from './questions/calculus.js'

const kExamDuration = 2 * 60 * 1_000

export const POST = async ({ request }) => {
    const body = await request.json()

    const validation = Joi.object({
        studentName: Joi.string().min(5).max(25)
    }).required().validate(body)

    if (validation.error) {
        return json({ error: validation.error.message }, { status: 422 })
    }

    const questions = shuffle([
        generateDerivativeQuestion(),
        ...Array.from({ length: 24 }, generateNonsenseQuestion)
    ])

    const normalizedName = body.studentName.trim()

    const exam = {
        studentName: normalizedName,
        examRef: await encrypt({
            examId: randomUUID(),
            studentName: normalizedName.toLowerCase(),
            endTime: new Date(Date.now() + kExamDuration).getTime(),
            answers: questions.map(question => question.answer)
        }, 'examData'),
        questions: questions.map(question => ({
            problemStatement: question.problemStatement,
            choices: question.choices
        }))
    }

    return json(exam)
}
