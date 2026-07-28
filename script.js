// ---------- заклёпки на дверях ----------
function buildRivets(container){
  const positions = [
    [8,8],[50,8],[92,8],
    [8,30],[92,30],
    [8,50],[92,50],
    [8,70],[92,70],
    [8,92],[50,92],[92,92]
  ];
  positions.forEach(([x,y])=>{
    const r = document.createElement('div');
    r.className = 'rivet';
    r.style.left = x+'%';
    r.style.top = y+'%';
    r.style.transform = 'translate(-50%,-50%)';
    container.appendChild(r);
  });
}
buildRivets(document.getElementById('rivetsLeft'));
buildRivets(document.getElementById('rivetsRight'));

// ---------- открытие врат ----------
const gate = document.getElementById('gate');
const library = document.getElementById('library');
let opened = false;

function openGate(){
  if(opened) return;
  opened = true;
  gate.classList.add('open');
  library.classList.add('show');
  document.getElementById('rainWindow').classList.add('show');
  setTimeout(()=>{
    gate.classList.add('hidden');
  }, 1950);
}

document.getElementById('doorLeft').addEventListener('click', openGate);
document.getElementById('doorRight').addEventListener('click', openGate);

// ---------- книги ----------
const books = [
  {
    title:"Локвуд и Компания",
    author:"Джонатан Страуд",
    emblem:"🗡️",
    desc:"Лондон наводнён призраками, и бороться с ними могут только дети — их чувства к сверхъестественному острее взрослых. Люси Карлайл поступает в маленькое агентство Локвуда, где вместе с харизматичным Энтони Локвудом и ироничным Джорджем они берутся за самые опасные дела, вооружившись рапирами, солью и железными опилками."
  },
  {
    title:"Школа Добра и Зла",
    author:"Соман Чайнани",
    emblem:"⚔️",
    desc:"Каждые несколько лет из деревни Гавалдон бесследно исчезают двое детей, чтобы попасть в таинственную Школу Добра и Зла. Софи мечтает стать принцессой, а Агата уверена, что годится лишь в злодейки — но судьба переворачивает их ожидания, распределяя девочек в противоположные башни."
  },
  {
    title:"Ты — угроза А-класса",
    author:"Данияр Сугралинов",
    emblem:"🎮",
    desc:"Мир внезапно превращается в подобие игры: у людей появляются уровни, характеристики и умения, а по улицам бродят монстры. Герою предстоит выживать по новым правилам реальности, стремительно набирая силу и постепенно осознавая, что сам он — угроза, которую боятся системы."
  },
  {
    title:"Легенда о Тёмном Эльфе",
    author:"Роберт Сальваторе",
    emblem:"🗡️",
    desc:"История происхождения Дриззта До'Урдена — тёмного эльфа, рождённого в жестоком подземном городе дроу, где правят предательство и культ Паучьей Королевы. Отвергая жестокость собственного народа, Дриззт выбирает путь чести, даже если это означает вечное изгнание."
  },
  {
    title:"Анимоксы",
    author:"Кристиан Хумберг, Тобиас Бахман",
    emblem:"🦉",
    desc:"Существуют звери, способные принимать облик людей, — анимоксы. Когда мир этих оборотней оказывается под угрозой, юным героям приходится вступить в тайное общество защитников и разгадать заговор, угрожающий стереть границу между человеком и зверем."
  },
  {
    title:"1984",
    author:"Джордж Оруэлл",
    emblem:"👁️",
    desc:"Тоталитарное государство Океания следит за каждым шагом и даже мыслью своих граждан через культ Старшего Брата. Уинстон Смит, сотрудник Министерства Правды, переписывающий историю по указке партии, решается на немыслимое — на собственные мысли и чувства."
  },
  {
    title:"Шестёрка Воронов",
    author:"Ли Бардуго",
    emblem:"🃏",
    desc:"В портовом городе Кеттердам собирается банда из шести изгоев — вор, стрелок, шпионка, снайпер и другие мастера своего опасного ремесла. Им предстоит невозможное ограбление, за которое никто в здравом уме не взялся бы, но награда стоит любого риска."
  },
  {
    title:"Часодеи",
    author:"Наталья Щерба",
    emblem:"⏳",
    desc:"Обычная девочка Василиса неожиданно узнаёт, что способна останавливать время, — а значит, принадлежит к древнему роду часодеев. Ей открывается скрытый мир волшебных часовых механизмов и городов, где ход времени можно замедлить, ускорить или повернуть вспять, но за каждый дар приходится платить."
  },
  {
    title:"Леворукие Книготорговцы Лондона",
    author:"Гарт Никс",
    emblem:"📖",
    desc:"В альтернативном Лондоне древний орден книготорговцев тайно охраняет границу между обыденным миром и миром мифов: левши сражаются с потусторонними существами, правши хранят знания. Когда девушка Сьюзен начинает искать своего таинственного отца, ей приходится довериться одному из этих загадочных книготорговцев."
  },
  {
    title:"Терра и Тайна Созвездий",
    author:"Мая Сара",
    emblem:"✨",
    desc:"В мире, где магический дар получают все, рождённые под знаком своего созвездия, Терра остаётся единственной без всяких способностей — пока однажды в ней не пробуждается пугающая сила. Вместе с изгоем Греем, рождённым под опальным знаком Змееносца, она отправляется на поиски книги Зодиаков, чтобы раскрыть тайну своего происхождения."
  }
];

const grid = document.getElementById('booksGrid');
const palette = ['#4a2224','#233b2e','#2c2440','#3a2a17','#1f2f3d','#3d1f1f','#2a2a2a','#1f3d3a','#402a1f','#33264a'];

books.forEach((b, i)=>{
  const card = document.createElement('div');
  card.className = 'book';
  card.style.background = `linear-gradient(160deg, ${palette[i % palette.length]}, #100d0a)`;
  card.innerHTML = `
    <div class="book-spine-lines"></div>
    <div>
      <div class="book-title">${b.title}</div>
      <div class="book-author">${b.author}</div>
    </div>
    <div class="book-emblem">${b.emblem}</div>
  `;
  card.addEventListener('click', ()=> openModal(b));
  grid.appendChild(card);
});

// ---------- модалка ----------
const overlay = document.getElementById('overlay');
function openModal(b){
  document.getElementById('modalEmblem').textContent = b.emblem;
  document.getElementById('modalTitle').textContent = b.title;
  document.getElementById('modalAuthor').textContent = b.author;
  document.getElementById('modalDesc').textContent = b.desc;
  overlay.classList.add('active');
}
function closeModal(){
  overlay.classList.remove('active');
}
document.getElementById('closeModal').addEventListener('click', closeModal);
overlay.addEventListener('click', (e)=>{
  if(e.target === overlay) closeModal();
});
document.addEventListener('keydown', (e)=>{
  if(e.key === 'Escape') closeModal();
});

// ---------- дождь за окном ----------
const dropsContainer = document.getElementById('drops');
function spawnDrops(count){
  for(let i=0;i<count;i++){
    const d = document.createElement('div');
    d.className = 'drop';
    const left = Math.random()*100;
    const height = 14 + Math.random()*22;
    const duration = 0.55 + Math.random()*0.85;
    const delay = Math.random()*2.5;
    d.style.left = left+'%';
    d.style.height = height+'px';
    d.style.animationDuration = duration+'s';
    d.style.animationDelay = delay+'s';
    d.style.opacity = (0.35 + Math.random()*0.5).toFixed(2);
    dropsContainer.appendChild(d);
  }
}
spawnDrops(45);

// ---------- молния ----------
function lightningStrike(){
  const wLight = document.getElementById('windowLightning');
  const pFlash = document.getElementById('pageFlash');
  wLight.classList.remove('flash');
  void wLight.offsetWidth;
  wLight.classList.add('flash');
  if(Math.random() < 0.45){
    pFlash.classList.remove('flash');
    void pFlash.offsetWidth;
    pFlash.classList.add('flash');
  }
  setTimeout(lightningStrike, 5000 + Math.random()*9000);
}
setTimeout(lightningStrike, 4000);
