(function(){
  var dd=document.querySelector('.nav-dd');
  if(!dd)return;
  var btn=dd.querySelector('.nav-dd-btn');
  btn.addEventListener('click',function(e){
    e.stopPropagation();
    dd.classList.toggle('open');
    btn.setAttribute('aria-expanded',dd.classList.contains('open'));
  });
  document.addEventListener('click',function(){dd.classList.remove('open');btn.setAttribute('aria-expanded','false');});
  var path=location.pathname.replace(/\.html$/,'').replace(/\/$/,'')||'/dashboard';
  dd.querySelectorAll('.nav-dd-menu a').forEach(function(a){
    var href=a.getAttribute('href').replace(/\.html$/,'').replace(/\/$/,'');
    if(path.endsWith(href)||href.endsWith(path.split('/').pop())) a.classList.add('current');
  });
  var lo=document.getElementById('logoutBtn');
  if(lo) lo.addEventListener('click',function(){
    fetch('/api/logout',{method:'POST'}).then(function(){location.href='/dashboard';});
  });
})();
