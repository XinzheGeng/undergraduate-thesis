import {get, post} from './fetch'

export function stat() {
    return get('/stat')
}

export function identifyMail(mail) {
    return post('/identify', {data: mail})
}
