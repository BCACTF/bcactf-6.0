import crypto from 'node:crypto'

// get it with sql injection on search
const hash = Buffer.from('666233353964316162363434636230653962366164333364336461653337303938652236d5', 'hex')

const salt = hash.subarray(0,17*2)
const interestingPart = hash.subarray(17*2).toString('hex')
console.log(interestingPart)
while (true) {
    const test = crypto.randomBytes(16).toString('hex')
    if (crypto.createHash('sha1').update(Buffer.concat([salt,Buffer.from(test,'utf8')])).digest('hex').startsWith(interestingPart)) {
        throw new Error(test)
    }
}
