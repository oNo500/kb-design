const {test}=require('node:test');const assert=require('node:assert/strict');
const {rowsFor}=require('../plugins/label-provenance/labels.js');
test('model evidence remains visible and cannot leak across concept identities',()=>{
 const records=[{uri:'urn:a',accept:true,label:'甲',language:'zh',property:'http://www.w3.org/2004/02/skos/core#prefLabel',
 basis:{level:5,model:{name:'test-model',date:'2026-09-13',rationale:'fixture',approval:'fixture only'}}}];
 assert.equal(rowsFor({schema_version:1,records},'urn:b').length,0);
 assert.match(rowsFor({schema_version:1,records},'urn:a')[0].notice,/外部用法未核实/);
 records[0].accept=false;assert.equal(rowsFor({schema_version:1,records},'urn:a').length,0);
});
test('local edits are shown as local input rather than external or AI evidence',()=>{
 const data={schema_version:1,records:[],local_records:[{uri:'urn:a',label:'本地名',language:'zh',property:'http://www.w3.org/2004/02/skos/core#prefLabel',edit_id:'edit',reason:'用户修改'}]};
 assert.match(rowsFor(data,'urn:a')[0].notice,/本地编辑/);
 assert.equal(rowsFor(data,'urn:b').length,0);
});
