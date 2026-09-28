import { render } from 'preact';
import { useEffect, useState } from 'preact/hooks';
import { useStore } from './store.js';
import { Home, Help } from './views/Home.jsx';
import { Mock, Practice } from './views/Setup.jsx';
import { Results, Review, Test } from './views/Test.jsx';
import { Guide } from './views/Guide.jsx';
import { Maps } from './views/Maps.jsx';
import { Cards } from './views/Cards.jsx';
import { Browse, Stats } from './views/Browse.jsx';

function useHash() {
  const [hash, setHash] = useState(() => window.location.hash || '#/');
  useEffect(() => {
    const on = () => setHash(window.location.hash || '#/');
    window.addEventListener('hashchange', on);
    return () => window.removeEventListener('hashchange', on);
  }, []);
  return hash;
}

function route(hash, store) {
  const parts = hash.replace(/^#\/?/, '').split('/').filter(Boolean).map(decodeURIComponent);
  const [head, a, b] = parts;
  switch (head) {
    case undefined:
      return <Home store={store} />;
    case 'help':
      return <Help />;
    case 'mock':
      return <Mock store={store} />;
    case 'practice':
      return <Practice store={store} />;
    case 'test':
      return <Test store={store} />;
    case 'results':
      return <Results store={store} id={a} />;
    case 'review':
      return <Review index={Number(a) || 0} />;
    case 'guide':
      return <Guide store={store} slug={a} objective={b} />;
    case 'maps':
      return <Maps store={store} id={a} />;
    case 'cards':
      return <Cards store={store} id={a} />;
    case 'browse':
      return <Browse store={store} id={a} />;
    case 'stats':
      return <Stats store={store} />;
    default:
      // A bare anchor from a shared link (e.g. #stats) maps to its page.
      if (['help', 'mock', 'practice', 'guide', 'maps', 'cards', 'browse', 'stats'].includes(hash.slice(1))) {
        window.location.hash = `#/${hash.slice(1)}`;
        return null;
      }
      return <Home store={store} />;
  }
}

function App() {
  const store = useStore();
  const hash = useHash();
  const isHome = hash === '#/' || hash === '#' || hash === '';
  const inTest = hash.startsWith('#/test');

  useEffect(() => {
    // New page: start at the top unless a guide link targets an objective.
    if (!/^#\/guide\/[^/]+\/./.test(hash)) window.scrollTo(0, 0);
  }, [hash]);

  return (
    <>
      {route(hash, store)}
      {!isHome && !inTest && (
        <a class="home-btn" href="#/">
          Home
        </a>
      )}
    </>
  );
}

// The app manages scroll itself (top of each page, or the linked objective).
try {
  history.scrollRestoration = 'manual';
} catch {
  /* not supported */
}

render(<App />, document.getElementById('app'));
