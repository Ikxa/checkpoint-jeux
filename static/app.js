const english=document.documentElement.lang==='en';
const cards=[...document.querySelectorAll('.card')];
function filter(){const q=document.querySelector('#search').value.toLocaleLowerCase(english?'en':'fr');const kind=document.querySelector('#kind').value;let count=0;for(const card of cards){card.hidden=Date.parse(card.dataset.until)<=Date.now()||!card.textContent.toLocaleLowerCase(english?'en':'fr').includes(q)||(kind!=='all'&&card.dataset.kind!==kind);if(!card.hidden)count++;}document.querySelector('#count').textContent=count+(english?' offers':' offres');document.querySelector('#empty').hidden=count>0;}
document.querySelector('#search').addEventListener('input',filter);document.querySelector('#kind').addEventListener('change',filter);filter();setInterval(filter,60000);
