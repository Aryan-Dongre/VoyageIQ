
  // Navbar scroll state
  const vqNavbar = document.getElementById('vqNavbar');
  function vqHandleScroll(){
    if(window.scrollY > 12){
      vqNavbar.classList.add('vq-scrolled');
    } else {
      vqNavbar.classList.remove('vq-scrolled');
    }
  }
  window.addEventListener('scroll', vqHandleScroll, { passive:true });
  vqHandleScroll();

  // Scroll reveal
  (function(){
    const reveals = document.querySelectorAll('.vq-reveal');
    if(!('IntersectionObserver' in window) || reveals.length === 0) return;
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if(entry.isIntersecting){
          entry.target.classList.add('vq-visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.15, rootMargin: '0px 0px -40px 0px' });
    reveals.forEach(el => observer.observe(el));
  })();
