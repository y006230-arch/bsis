module.exports = async (req, res) => {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'POST만 허용됩니다.' });
  }
  const secure = process.env.VERCEL === '1' || process.env.NODE_ENV === 'production';
  const cookie = [
    'bsis_auth=',
    'HttpOnly',
    'Path=/',
    'SameSite=Strict',
    'Max-Age=0',
    secure ? 'Secure' : '',
  ]
    .filter(Boolean)
    .join('; ');
  res.setHeader('Set-Cookie', cookie);
  return res.status(200).json({ ok: true, redirect: '/dashboard' });
};
