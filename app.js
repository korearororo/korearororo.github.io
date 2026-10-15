const toggle = document.querySelector('.menu-toggle');
const navigation = document.querySelector('#navigation');
if (toggle && navigation) {
  const closeMenu = () => {
    toggle.setAttribute('aria-expanded', 'false');
    toggle.setAttribute('aria-label', '메뉴 열기');
    navigation.classList.remove('is-open');
  };
  toggle.addEventListener('click', () => {
    const open = toggle.getAttribute('aria-expanded') !== 'true';
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? '메뉴 닫기' : '메뉴 열기');
    navigation.classList.toggle('is-open', open);
  });
  navigation.querySelectorAll('a').forEach(a => a.addEventListener('click', closeMenu));
  document.addEventListener('keydown', e => { if (e.key === 'Escape') closeMenu(); });
}
document.querySelectorAll('.print-button').forEach(button => button.addEventListener('click', () => window.print()));

document.querySelectorAll('[data-seek]').forEach(button => button.addEventListener('click', () => {
  const video = button.closest('section').querySelector('video');
  if (!video) return;
  const seekAndPlay = () => {
    video.currentTime = Number(button.dataset.seek);
    video.play().catch(() => {});
  };
  if (video.readyState >= 1) seekAndPlay();
  else {
    video.addEventListener('loadedmetadata', seekAndPlay, { once: true });
    video.load();
  }
}));
