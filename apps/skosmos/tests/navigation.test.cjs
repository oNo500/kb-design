const {test} = require('node:test');
const assert = require('node:assert/strict');
const {roots, children} = require('../overrides/navigation.js');
function fixture() {
 const node = (name, kids, parents) => ({labels:{en:name},notation:'',children:kids,parents});
 return {nodes:{a:node('A',['b','outside'],['b']),b:node('B',['a'],['a']),outside:node('Outside',[],['a'])},
 schemes:{s:{labels:{en:'Scheme'},members:['a','b'],entries:[],unconnected:['a','b'],explicit:false}}};
}
test('cycles terminate along each displayed path without leaking other-scheme children', () => {
 const nav=fixture(), scheme=roots(nav,'en')[0];
 const a=children(nav,scheme,'en')[0];
 const b=children(nav,a,'en'); assert.deepEqual(b.map(x=>x.uri),['b']);
 const repeated=children(nav,b[0],'en')[0]; assert.equal(repeated.uri,'a');assert.equal(repeated.hasChildren,false);
});
test('selected concepts remain reachable when no source top concepts exist', () => {
 const nav=fixture(); const scheme=roots(nav,'en','b')[0];
 assert.equal(scheme.isOpen,true);assert.ok(scheme.children.some(x=>x.uri==='b'));
 assert.match(scheme.navigationNote,/不代表来源指定顶层/);
});
test('empty schemes do not show an expansion arrow; missing labels fall back to URI', () => {
 const nav=fixture();nav.schemes.s.members=[];nav.schemes.s.labels={};
 const scheme=roots(nav,'en')[0];assert.equal(scheme.hasChildren,false);assert.equal(scheme.label,'s');
});
