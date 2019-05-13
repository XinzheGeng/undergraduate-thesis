import {post} from './fetch'

export function identifyMail(mail) {
    return post('/identify', {data: mail})
}
