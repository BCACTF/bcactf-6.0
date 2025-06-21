import { redirect } from '@sveltejs/kit'

import { readFileSync } from 'fs'

import sharp from 'sharp'

import { decrypt } from '$lib/encryption.js'

const angryWomanSvg = readFileSync('private/angrywoman.svg', 'utf-8')

const renderAngryWoman = async results => {
    let updatedSvg = angryWomanSvg

    for (let i = 1; i <= 25; i++) {
        let replaceIndex

        switch (results[i - 1]) {
            case '1':
                replaceIndex = updatedSvg.indexOf(`id="x${i}"`)
                break
            case '0':
                replaceIndex = updatedSvg.indexOf(`id="ch${i}"`)
                break
        }

        const before = updatedSvg.slice(0, replaceIndex)
        const after = updatedSvg.slice(replaceIndex)

        // lol
        updatedSvg = before + after.replace('style="', 'style="stroke-opacity:0;')
    }

    return (await sharp(Buffer.from(updatedSvg, 'utf-8'))
        .resize(null, 500)
        .toFormat('webp')
        .toBuffer()).toString('base64')
}

export const actions = {
    default: async ({ locals, request }) => {
        locals.didRunGrading = true

        const data = await request.formData()

        const resultsRef = data.get('resultsRef')

        let examResults

        try {
            examResults = await decrypt(resultsRef, 'examResults')
        } catch {
            return { status: 'malformed' }
        }

        if (examResults.expires < new Date()) {
            return { status: 'expired' }
        } else if (examResults.studentName !== 'timmy bobbins') {
            return { status: 'unknownStudent' }
        } else if (!examResults.results.includes('0')) {
            return {
                status: 'pass',
                flag: readFileSync('private/flag.txt', 'utf-8')
            }
        }

        const png = await renderAngryWoman(examResults.results)

        return {
            status: 'fail',
            angryWoman: `data:image/webp;base64,${png}`
        }
    }
}

export const load = ({ locals }) => {
    if (!locals.didRunGrading) {
        redirect(307, '/')
    }
}

export const csr = false
