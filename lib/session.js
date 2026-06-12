const crypto = require('crypto');

function b64url(buf) {
  return Buffer.from(buf).toString('base64url');
}

function fromB64url(str) {
  return Buffer.from(str, 'base64url');
}

function getSecret() {
  const s = process.env.AUTH_SECRET;
  if (!s) throw new Error('AUTH_SECRET not configured');
  return s;
}

function sign(payloadObj) {
  const secret = getSecret();
  const payload = b64url(JSON.stringify(payloadObj));
  const sig = crypto.createHmac('sha256', secret).update(payload).digest('base64url');
  return payload + '.' + sig;
}

function verify(token) {
  if (!token || !token.includes('.')) return null;
  const [payload, sig] = token.split('.');
  const secret = getSecret();
  const expected = crypto.createHmac('sha256', secret).update(payload).digest('base64url');
  if (sig !== expected) return null;
  try {
    const data = JSON.parse(fromB64url(payload).toString('utf8'));
    if (!data.exp || Date.now() > data.exp) return null;
    return data;
  } catch {
    return null;
  }
}

function getClientIp(req) {
  const xf = req.headers['x-forwarded-for'];
  if (xf) return String(xf).split(',')[0].trim();
  if (req.headers['x-real-ip']) return String(req.headers['x-real-ip']).trim();
  return req.socket?.remoteAddress || '';
}

function getAllowedIps() {
  return (process.env.ALLOWED_IPS || '')
    .split(',')
    .map((s) => s.trim())
    .filter(Boolean);
}

function isIpAllowed(ip) {
  const allowed = getAllowedIps();
  if (!allowed.length) return false;
  return allowed.includes(ip);
}

function createSessionToken(username, ip, maxAgeSec) {
  const exp = Date.now() + maxAgeSec * 1000;
  return sign({ u: username, ip, exp });
}

module.exports = {
  sign,
  verify,
  getClientIp,
  getAllowedIps,
  isIpAllowed,
  createSessionToken,
};
