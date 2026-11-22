// Door pages of "A Crusader's Christmas".
// Door N opens on DOOR_YEAR-12-N (local date) and stays open; later doors show when they open.
// The date that counts as today can be set for tests with "map-availability-date" (YYYY-MM-DD),
// the same key that dates the maps in the game, read in the same order as the game: the
// maploader's value wins over the files module's, and an empty maploader value clears it.
// The page only reads; it never changes the configuration.

const CalendarLogic = (() => {
  const PLUGIN_NAME = 'ChristmasCalendar';
  const DOOR_COUNT = 21;
  const DOOR_YEAR = 2026;
  const STORY_DOORS = [1, 6, 8, 15];
  const RTL_LANGUAGES = ['fa'];
  // GUI language codes that are not BCP 47 tags
  const DATE_LOCALES = { ch: 'zh-CN', fa: 'fa-IR' };
  const MAP_NAMES = { en: 'Door', de: 'Türchen' };

  function pad(n) {
    return String(n).padStart(2, '0');
  }

  const DAYS_IN_MONTH = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];

  function isLeapYear(y) {
    return (y % 4 === 0 && y % 100 !== 0) || y % 400 === 0;
  }

  // "YYYY-MM-DD" (a real calendar date) -> yyyymmdd, or null (same rules as the files module)
  function parseDate(value) {
    if (typeof value !== 'string') return null;
    const m = value.match(/^(\d{4})-(\d{2})-(\d{2})$/);
    if (!m) return null;
    const y = Number(m[1]);
    const mo = Number(m[2]);
    const d = Number(m[3]);
    if (y < 1 || mo < 1 || mo > 12 || d < 1) return null;
    const days = mo === 2 && isLeapYear(y) ? 29 : DAYS_IN_MONTH[mo - 1];
    if (d > days) return null;
    return y * 10000 + mo * 100 + d;
  }

  // The preview date the game uses: the maploader's value if it has one (an empty value clears
  // it), otherwise the files module's. Returns yyyymmdd or null.
  function previewDate(filesValue, maploaderValue) {
    const selected = maploaderValue !== undefined && maploaderValue !== null ? maploaderValue : filesValue;
    if (selected === undefined || selected === null || selected === '') return null;
    return parseDate(selected);
  }

  function dateKey(date) {
    return date.getFullYear() * 10000 + (date.getMonth() + 1) * 100 + date.getDate();
  }

  function doorOpensOn(n) {
    return DOOR_YEAR * 10000 + 12 * 100 + n;
  }

  function doorIsOpen(n, today) {
    return today >= doorOpensOn(n);
  }

  function doorId(n) {
    return `Door${pad(n)}`;
  }

  function mapName(n, mapLanguage) {
    return `${MAP_NAMES[mapLanguage] ?? MAP_NAMES.en}${pad(n)}`;
  }

  // The intro file for the language, else the English one. `available` holds the file names found.
  function introFile(n, language, available) {
    const id = doorId(n);
    const wanted = `${id}_${language}.html`;
    if (available.has(wanted)) return wanted;
    return `${id}_en.html`;
  }

  function isRtl(language) {
    return RTL_LANGUAGES.includes(language);
  }

  function formatDate(key, language, withYear = true) {
    const date = new Date(Math.floor(key / 10000), Math.floor(key / 100) % 100 - 1, key % 100);
    const options = withYear ? { day: 'numeric', month: 'long', year: 'numeric' } : { day: 'numeric', month: 'long' };
    try {
      return date.toLocaleDateString(DATE_LOCALES[language] ?? language, options);
    } catch (e) {
      return `${Math.floor(key / 10000)}-${pad(Math.floor(key / 100) % 100)}-${pad(key % 100)}`;
    }
  }

  function fill(template, values) {
    return String(template).replace(/\{(\w+)\}/g, (all, name) => (name in values ? values[name] : all));
  }

  return {
    PLUGIN_NAME,
    DOOR_COUNT,
    DOOR_YEAR,
    STORY_DOORS,
    parseDate,
    previewDate,
    dateKey,
    doorOpensOn,
    doorIsOpen,
    doorId,
    mapName,
    introFile,
    isRtl,
    formatDate,
    fill,
  };
})();

if (typeof SANDBOX_FUNCTIONS !== 'undefined') {
  // nothing to save; returning an object keeps "Save" harmless
  SANDBOX_FUNCTIONS.getConfig = () => ({});
}

const CalendarPage = (() => {
  const L = CalendarLogic;
  const state = {
    language: 'en',
    mapLanguage: 'en',
    today: 0,
    root: null, // game-relative folder of the installed plugin
    files: new Set(), // file names below doors/
    strings: {},
    selected: null,
  };

  async function text(id, fallback) {
    if (state.strings[id] === undefined) {
      let value = null;
      try {
        value = await HOST_FUNCTIONS.getLocalizedString(id);
      } catch (e) {
        value = null;
      }
      state.strings[id] = value || fallback || id;
    }
    return state.strings[id];
  }

  async function configValue(url) {
    try {
      return await HOST_FUNCTIONS.getConfigState(url);
    } catch (e) {
      return undefined;
    }
  }

  async function findPluginFiles() {
    const found = await HOST_FUNCTIONS.receivePluginPaths('doors', '**/*');
    const own = (found || []).find((entry) => entry.description && entry.description.name === L.PLUGIN_NAME);
    if (!own) return;
    state.root = own.path;
    for (const path of own.paths || []) {
      state.files.add(path.split('/').pop());
    }
  }

  function doorPath(n, file) {
    return `${state.root}/doors/${L.doorId(n)}/${file}`;
  }

  // The intros use only these elements; a span may carry a colour for a lord's name.
  const INTRO_TAGS = new Set(['P', 'BR', 'DETAILS', 'SUMMARY', 'EM', 'STRONG', 'SPAN']);
  const COLOUR = /^\s*color\s*:\s*(#[0-9a-f]{3}|#[0-9a-f]{6}|[a-z]{3,20})\s*;?\s*$/i;

  // Builds a new fragment from the intro: allowed elements are copied (other elements are
  // replaced by their text and children), with no attributes except a validated colour.
  function cleanHtml(html) {
    const doc = new DOMParser().parseFromString(`<div>${html}</div>`, 'text/html');
    const source = doc.body.firstElementChild;
    const out = document.createElement('div');
    function copy(from, to) {
      for (const node of from.childNodes) {
        if (node.nodeType === 3) {
          to.appendChild(document.createTextNode(node.nodeValue));
        } else if (node.nodeType === 1) {
          if (INTRO_TAGS.has(node.tagName.toUpperCase())) {
            const element = document.createElement(node.tagName.toLowerCase());
            if (node.tagName.toUpperCase() === 'SPAN') {
              const match = COLOUR.exec(node.getAttribute('style') || '');
              if (match) element.style.color = match[1];
            }
            copy(node, element);
            to.appendChild(element);
          } else if (!['SCRIPT', 'STYLE', 'TEMPLATE'].includes(node.tagName.toUpperCase())) {
            copy(node, to);
          }
        }
      }
    }
    if (source) copy(source, out);
    return out;
  }

  async function readIntro(n, file) {
    if (!state.root) return null;
    try {
      return await HOST_FUNCTIONS.getTextFile(doorPath(n, file));
    } catch (e) {
      return null;
    }
  }

  async function showDoor(n) {
    state.selected = n;
    document.querySelectorAll('.door').forEach((button) => {
      button.classList.toggle('selected', Number(button.dataset.door) === n);
    });

    const detail = document.getElementById('door-detail');
    const image = document.getElementById('door-preview');
    const target = document.getElementById('door-text');
    detail.hidden = false;
    image.hidden = true;
    image.removeAttribute('src');
    target.textContent = '';

    const title = L.fill(await text('door_title', 'Door {n}'), { n });
    const hint = L.fill(await text('door_map_hint', 'In the game: Custom Scenarios → Play a Map → {map}'), {
      map: L.mapName(n, state.mapLanguage),
    });
    if (state.selected !== n) return;
    document.getElementById('door-title').textContent = title;
    document.getElementById('door-map').textContent = hint;

    // the intro: the launcher language, else English
    let file = L.introFile(n, state.language, state.files);
    let language = file.endsWith(`_${state.language}.html`) ? state.language : 'en';
    let html = await readIntro(n, file);
    if (!html && language !== 'en') {
      file = `${L.doorId(n)}_en.html`;
      language = 'en';
      html = await readIntro(n, file);
    }
    if (state.selected !== n) return;
    target.lang = language;
    target.dir = L.isRtl(language) ? 'rtl' : 'ltr';
    if (html) {
      target.appendChild(cleanHtml(html));
    } else {
      target.textContent = await text('door_text_missing', 'The text for this door could not be loaded.');
    }

    // the overview picture is optional
    const previewFile = `${L.doorId(n)}_preview.jpg`;
    if (state.root && state.files.has(previewFile)) {
      let url = null;
      try {
        url = await HOST_FUNCTIONS.getAssetUrl(doorPath(n, previewFile));
      } catch (e) {
        url = null;
      }
      const alt = L.fill(await text('door_preview_alt', 'Overview of the map of door {n}'), { n });
      if (url && state.selected === n) {
        image.alt = alt;
        image.src = url;
        image.hidden = false;
      }
    }
  }

  async function renderDoors() {
    const list = document.getElementById('doors');
    list.textContent = '';
    const storyLabel = await text('story_badge', 'Story');
    const opensOn = await text('door_opens_on', 'Opens on {date}');
    let latestOpen = null;

    for (let n = 1; n <= L.DOOR_COUNT; n += 1) {
      const open = L.doorIsOpen(n, state.today);
      const button = document.createElement('button');
      button.type = 'button';
      button.dataset.door = String(n);
      button.setAttribute('role', 'listitem');
      button.className = `door ${open ? 'open' : 'closed'}`;

      const number = document.createElement('span');
      number.className = 'number';
      number.textContent = String(n);
      button.appendChild(number);

      if (L.STORY_DOORS.includes(n)) {
        const story = document.createElement('span');
        story.className = 'story';
        story.textContent = '★';
        story.title = storyLabel;
        button.appendChild(story);
      }

      if (open) {
        latestOpen = n;
        button.onclick = () => showDoor(n);
      } else {
        const label = document.createElement('span');
        label.className = 'label';
        label.textContent = L.fill(opensOn, { date: L.formatDate(L.doorOpensOn(n), state.language, false) });
        button.appendChild(label);
        button.disabled = true;
      }
      list.appendChild(button);
    }
    return latestOpen;
  }

  async function init() {
    try {
      state.language = (await HOST_FUNCTIONS.getLanguage()) || 'en';
    } catch (e) {
      state.language = 'en';
    }
    const calendar = document.getElementById('calendar');
    calendar.lang = state.language;
    calendar.dir = L.isRtl(state.language) ? 'rtl' : 'ltr';

    const mapLanguage = await configValue(`${L.PLUGIN_NAME}.map-language`);
    state.mapLanguage = mapLanguage === 'de' ? 'de' : 'en';

    state.today = L.dateKey(new Date());
    const preview = L.previewDate(
      await configValue('files.map-availability-date'),
      await configValue('maploader.map-availability-date'),
    );
    if (preview !== null) {
      state.today = preview;
      const note = document.getElementById('preview-date');
      note.textContent = L.fill(
        await text('preview_date_active', 'Showing the calendar as on {date} (setting map-availability-date).'),
        { date: L.formatDate(preview, state.language) },
      );
      note.hidden = false;
    }

    try {
      await findPluginFiles();
    } catch (e) {
      state.root = null;
    }

    const latestOpen = await renderDoors();
    if (latestOpen !== null) {
      await showDoor(latestOpen);
    }
  }

  return { init, state, cleanHtml };
})();

if (typeof addEventListener !== 'undefined') {
  addEventListener('INIT_DONE', () => {
    CalendarPage.init();
  });
}

if (typeof module !== 'undefined') {
  module.exports = { CalendarLogic, CalendarPage };
}
