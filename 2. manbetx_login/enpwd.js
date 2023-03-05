RSAFile = require('./rsa')

function enpwd(pwd) {
    var rsaKey = new RSAFile.RSAKey();
    rsaKey.setPublic(RSAFile.b64tohex('ALk9dqw5X2JguUTJbSpaDckwAmcePQXhGb3W+0wJD/5Y35Ad8LVpqLtkg7jb8qhLVyGKTvH0GMXsj/NiSISnDCqJwtL4IxM8GIY4JUu/BeRwoQ6/EufYFCE3S7PupEaHXBi6Kq4knpBnWy012tVOr4Ag9pUElsN2Joq8Foj6xxrZ'), RSAFile.b64tohex('AQAB'));
    return RSAFile.hex2b64(rsaKey.encrypt(pwd))
}

console.log(enpwd('1'));