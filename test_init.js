// Runtime smoke test for index.html: a minimal DOM stub that actually EXECUTES the
// embedded init JS (not just parses it) and exercises every interactive path.
// `new Function(js)` only checks syntax and MISSED a TDZ bug (const used before init),
// so always run this after build_site.py:   node test_init.js
const fs = require('fs');
const path = require('path');
const t = fs.readFileSync(path.join(__dirname, 'index.html'), 'utf8');
const js = t.slice(t.indexOf('<script>') + 8, t.lastIndexOf('</script>'));

class El {
  constructor(tag='div'){this.tag=tag;this._children=[];this.style={};this.dataset={};this._value=undefined;this._tc='';this._html='';
    this.classList={toggle(){},add(){},remove(){},contains(){return false;}};}
  get textContent(){return this._tc;} set textContent(v){this._tc=String(v);}
  get innerHTML(){return this._html;} set innerHTML(v){this._html=String(v); if(v==='')this._children=[];}
  appendChild(c){this._children.push(c);return c;}
  get lastElementChild(){return this._children[this._children.length-1];}
  get children(){return this._children;}
  get options(){const out=[];const walk=n=>{(n._children||[]).forEach(ch=>{if(ch.tag==='option')out.push(ch);walk(ch);});};walk(this);return out;}
  get value(){if(this._value!==undefined&&this._value!=='')return this._value;const o=this.options[0];return o?o.value:'';}
  set value(v){this._value=v;}
  querySelectorAll(){return [];}
  addEventListener(){}
  set onclick(f){this._onclick=f;} get onclick(){return this._onclick;}
  set onchange(f){this._onchange=f;} get onchange(){return this._onchange;}
  set oninput(f){this._oninput=f;} get oninput(){return this._oninput;}
  getAttribute(k){return this.dataset[k];}
  closest(){return null;}
}
const reg={};
global.document={getElementById(id){if(!reg[id])reg[id]=new El('#'+id);return reg[id];},createElement(tag){return new El(tag);},addEventListener(){},querySelectorAll(){return [];}};
global.window=global; global.localStorage={getItem(){return null;},setItem(){}}; global.setTimeout=()=>0;

function fire(id, ev){const el=reg[id]; if(!el)return; const h=el['_'+ev]; if(h)h();}
try {
  (0, eval)(js);
  const spot=reg['spot'], grid=reg['grid'];
  if(spot.options.length<10 || grid._children.length!==169) throw new Error('init produced empty chart (spots='+spot.options.length+', cells='+grid._children.length+')');
  console.log('INIT ok: spots='+spot.options.length+' cells='+grid._children.length);
  reg['cfg']._value='EDGE Push/Fold (Nash, +1bb ante)'; fire('cfg','onchange');
  console.log('config switch ok: spots='+spot.options.length);
  fire('tabQuiz','onclick');  if(!reg['ptable']._html||reg['ptable']._html.indexOf('seat')<0) throw new Error('strategy quiz table empty');
  fire('qChartBtn','onclick'); if(reg['qcGrid']._children.length!==169) throw new Error('quiz-side chart not rendered ('+reg['qcGrid']._children.length+')');
  fire('qnext','onclick'); if(reg['qcGrid']._children.length!==169) throw new Error('quiz chart did not refresh on next');
  fire('qmPost','onclick'); if(!reg['pQuizBody']._html||reg['pQuizBody']._html.indexOf('pq-q')<0) throw new Error('postflop quiz not rendered');
  for(let z=0;z<25;z++) global.pickPost(); // exercise all postflop question types
  fire('qmSrp','onclick'); if(!reg['srpQuizBody']._html||reg['srpQuizBody']._html.indexOf('pq-q')<0) throw new Error('SRP strategy quiz not rendered');
  if(reg['srpQuizBody']._html.indexOf('pq-board')<0) throw new Error('SRP quiz has no flop (empty data?)');
  for(let z=0;z<40;z++){ if(reg['srpbtns'])reg['srpbtns']._children=[]; global.pickSrp(); const nb=reg['srpbtns']._children.length; if(nb<2) throw new Error('SRP quiz has <2 options'); global.answerSrp((Math.random()*nb)|0); if(reg['srpres']._html.indexOf('GTO頻度')<0) throw new Error('SRP grading not shown'); } // both sides (2- and 3-option) + grading
  console.log('SRP quiz ok: rendered board + 40 graded answers');
  fire('qmStrat','onclick');
  fire('qmTerm','onclick');   if(!reg['tprompt']._tc) throw new Error('term quiz empty');
  fire('qmStrat','onclick'); fire('qnext','onclick'); fire('tnext','onclick'); fire('qreview','onclick');
  fire('tabGloss','onclick'); if(reg['glist']._children.length<1) throw new Error('glossary empty');
  fire('tabCalc','onclick');
  if(!reg['cboard']._html||reg['cboard']._html.indexOf('cslot')<0) throw new Error('calc board not rendered');
  if(!reg['players']._html||reg['players']._html.indexOf('prow')<0) throw new Error('calc players not rendered');
  {const R='23456789TJQKA',SU={s:0,h:1,d:2,c:3},cd=x=>R.indexOf(x[0])*4+SU[x[1]];
   const eq=global.computeEquity([[cd('Qs'),cd('Jh')],[cd('9s'),cd('9h')],[cd('8s'),cd('7d')]],[cd('As'),cd('Ks'),cd('7c')]).map(x=>+x.equity.toFixed(2));
   if(Math.abs(eq[0]-39.65)>0.2||Math.abs(eq[1]-44.19)>0.2||Math.abs(eq[2]-16.17)>0.2) throw new Error('equity wrong: '+eq.join('/'));
   console.log('equity self-test ok:',eq.join(' / '));}
  fire('tabHowto','onclick');
  fire('tabChart','onclick');
  console.log('ALL PATHS ok ✓');
} catch(e) {
  console.error('FAIL:', e.message);
  console.error(e.stack.split('\n').slice(0,5).join('\n'));
  process.exit(1);
}
