import { createCipheriv, createDecipheriv, hkdf, randomBytes } from 'crypto'

import { env } from '$env/dynamic/private'

import { kEncryptionKey } from './security.server.js'

const kDisclaimer = Buffer.from(
    'don\'t try to decode this string it\'s seriously not part of the chall.',
    'utf-8'
)

const deriveKey = (salt, audience, cb) => new Promise((res, rej) => {
    hkdf('sha-256', kEncryptionKey, salt, audience, 32, (err, derivedKey) => {
        if (err) {
            return rej(err)
        }

        res(derivedKey)
    })
})

const encrypt = async (data, audience) => {
    const salt = randomBytes(16)

    const derivedKey = await deriveKey(salt, audience)

    const cipher = createCipheriv('aes-256-gcm', derivedKey, Buffer.alloc(12))

    return Buffer.concat([
        kDisclaimer,
        salt,
        cipher.update(JSON.stringify(data)),
        cipher.final(),
        cipher.getAuthTag()
    ]).toString('hex')
}

const decrypt = async (value, audience) => {
    if (!value.startsWith(kDisclaimer.toString('hex'))) {
        throw new Error()
    }

    const buffer = Buffer.from(value, 'hex').slice(kDisclaimer.length)

    const salt = buffer.slice(0, 16)
    const cipherText = buffer.slice(16, -16)
    const authTag = buffer.slice(-16)

    const derivedKey = await deriveKey(salt, audience)

    const decipher = createDecipheriv(
        'aes-256-gcm',
        derivedKey,
        Buffer.alloc(12)
    )

    decipher.setAuthTag(authTag)

    const plaintext = Buffer.concat([
        decipher.update(cipherText),
        decipher.final()
    ])

    return JSON.parse(plaintext.toString('utf-8'))
}

export { encrypt, decrypt }
