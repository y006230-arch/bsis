const {
  getClientIp,
  isIpAllowed,
  createSessionToken,
  getAllowedIps,
} = require('../lib/session');

const MAX_AGE = 60 * 60 * 12; // 12 hours

module.exports = async (req, res) => {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'POST만 허용됩니다.' });
  }

  const user = process.env.AUTH_USER;
  const pass = process.env.AUTH_PASSWORD;
  const secret = process.env.AUTH_SECRET;

  if (!user || !pass || !secret) {
    return res.status(500).json({
      error: '인증 환경변수(AUTH_USER, AUTH_PASSWORD, AUTH_SECRET)가 설정되지 않았습니다.',
    });
  }

  if (!getAllowedIps().length) {
    return res.status(500).json({
      error: '허용 IP(ALLOWED_IPS)가 설정되지 않았습니다.',
    });
  }

  let body = req.body;
  if (typeof body === 'string') {
    try {
      body = JSON.parse(body);
    } catch {
      body = {};
    }
  }
  body = body || {};

  const username = String(body.username || '').trim();
  const password = String(body.password || '');
  const clientIp = getClientIp(req);

  if (!isIpAllowed(clientIp)) {
    return res.status(403).json({
      error: '허용되지 않은 IP입니다. 관리자에게 IP 등록을 요청하세요.',
      ip: clientIp,
    });
  }

  if (username !== user || password !== pass) {
    return res.status(401).json({ error: '아이디 또는 비밀번호가 올바르지 않습니다.' });
  }

  let token;
  try {
    token = createSessionToken(username, clientIp, MAX_AGE);
  } catch (e) {
    return res.status(500).json({ error: e.message });
  }

  const secure = process.env.VERCEL === '1' || process.env.NODE_ENV === 'production';
  const cookie = [
    `bsis_auth=${token}`,
    'HttpOnly',
    'Path=/',
    'SameSite=Strict',
    `Max-Age=${MAX_AGE}`,
    secure ? 'Secure' : '',
  ]
    .filter(Boolean)
    .join('; ');

  res.setHeader('Set-Cookie', cookie);
  return res.status(200).json({ ok: true, redirect: '/손익요약_대시보드' });
};
