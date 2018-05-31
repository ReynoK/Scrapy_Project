import hashlib
import base64

def md5(s):
        h = hashlib.md5()
        h.update(s.encode(encoding='utf8'))
        return h.hexdigest()

def decode_base64(data):
        missing_padding = 4 - len(data) % 4
        if missing_padding:
                data += '='* missing_padding
        return str(base64.decodestring(data.encode('utf-8')),'utf-8')

def jandan_load_img(n, t):
        f = 'DECODE'
        e = 0
        r = 4
        t = md5(t)
        d = n
        p = md5(t[0:16])
        o = md5(t[16:32])

        if r:
                if f == 'DECODE':
                        m = n[0:r]

        else:
                m = ''

        c = p + md5(p + m)
        l = ''
        if f == 'DECODE':
                n = n[r:]
                l = decode_base64(n)
        k = list(range(256))
        b = [ord(c[g % len(c)]) for g in range(256)]
        g = 0
        for h in range(0,256):
                g = (g + k[h] + b[h]) % 256
                tmp = k[h]
                k[h] = k[g]
                k[g] = tmp
        u = ""

        q = 0
        g = 0
        for h in range(len(l)):
                q = (q+1)%256
                g = (g+k[q])%256
                tmp = k[q]
                k[q] = k[g]
                k[g] = tmp
                u += chr(ord(l[h]) ^ (k[(k[q] + k[g])%256]))
        u = u[26:]
        u = decode_base64(d)
        return u

