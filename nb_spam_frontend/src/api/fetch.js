import axios from 'axios'
import config from './config'

function getRealUrl(url) {
    if (!url.startsWith('http') || url.startsWith('/')) {
        if (config.baseUrl.endsWith('/')) {
            config.baseUrl = config.baseUrl.substring(
                0,
                config.baseUrl.length - 1
            )
        }
        if (!url.startsWith('/')) {
            url = '/' + url
        }
        return config.baseUrl + url
    }
    return url
}

export default function fetch(options) {
    return new Promise((resolve, reject) => {
        if (!reject) {
            reject = error => console.log(error)
        }
        const axiosInst = axios.create({
            headers: {
                'Content-Type': 'application/json',
            },
            timeout: 30 * 1000, // 30 seconds
        })
        axiosInst(options)
            .then(response => resolve(response))
            .catch(error => reject(error))
    })
}

export function get(url, options) {
    return fetch({
        method: 'get',
        url: getRealUrl(url),
        ...options,
    })
}

export function post(url, options) {
    return fetch({
        method: 'post',
        url: getRealUrl(url),
        ...options,
    })
}

export function put(url, options) {
    return fetch({
        method: 'put',
        url: getRealUrl(url),
        ...options,
    })
}

export function _delete(url, options) {
    return fetch({
        method: 'delete',
        url: getRealUrl(url),
        ...options,
    })
}
