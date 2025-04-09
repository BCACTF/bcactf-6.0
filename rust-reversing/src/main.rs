fn make_character_but_stupidly(char: char, offset: i16) -> char {
    let mut ret = char as i16;
    ret += offset;
    return ret as u8 as char;
}

fn yeet(flag: &mut Vec<char>) {
    flag.push(make_character_but_stupidly('a', 13));
    flag.push(make_character_but_stupidly('c', 13));
    flag.push(make_character_but_stupidly('t', 13));
    flag.push(make_character_but_stupidly('f', 13));
    flag.push(make_character_but_stupidly('{', 0));
    flag.push(make_character_but_stupidly('w', 13));
    flag.push(make_character_but_stupidly('0', 0));
    flag.push(make_character_but_stupidly('w', 13));
    flag.push(make_character_but_stupidly('_', 0));
    flag.push(make_character_but_stupidly('r', 13));
    flag.push(make_character_but_stupidly('U', 13));
    flag.push(make_character_but_stupidly('s', 13));
    flag.push(make_character_but_stupidly('T', 0));
    flag.push(make_character_but_stupidly('_', 0));
    flag.push(make_character_but_stupidly('r', 13));
    flag.push(make_character_but_stupidly('e', 13));
    flag.push(make_character_but_stupidly('v', 13));
    flag.push(make_character_but_stupidly('e', 13));
    flag.push(make_character_but_stupidly('r', 13));
    flag.push(make_character_but_stupidly('s', 13));
    flag.push(make_character_but_stupidly('e', 13));
    flag.push(make_character_but_stupidly('}', 0));
}

fn main() {
    let mut flaggie: Vec<char> = Vec::new();
    flaggie.push('b');
    flaggie.push('c');
    yeet(&mut flaggie);
    println!("go find the flag in ghidra");
}
