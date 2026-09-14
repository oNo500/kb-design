/* Display shared label evidence without changing vocabulary labels or RDF. */
(function (root) {
  function rowsFor(data, uri) {
    const local = (data?.local_records || []).filter(row => row.uri === uri).map(row => ({label: row.label, language: row.language, kind: '本地名称', notice: '本地编辑 · 未据此认定外部依据或术语准入', detail: `${row.edit_id} · ${row.reason}`}));
    if (data?.schema_version === 2) {
      return data.labels.filter(row => row.uri === uri).map(row => {
        const batch = data.batches[row.batch];
        return {label: row.label, language: row.language, kind: '首选名',
          notice: `AI 翻译 · ${batch.model}，未核对权威中文术语`,
          detail: `批次 ${row.batch} · ${batch.agent} · ${batch.output_written_at}`};
      }).concat(local);
    }
    if (!data || data.schema_version !== 1 || !Array.isArray(data.records)) throw new Error('Invalid label provenance');
    return data.records.filter(row => row.uri === uri && row.accept === true).map(row => ({
      label: row.label, language: row.language,
      kind: row.property.endsWith('#prefLabel') ? '首选名' : row.property.endsWith('#altLabel') ? '替代名' : '检索写法',
      notice: row.basis.level === 5 ? '模型知识 · 第 5 级，外部用法未核实' : `外部依据 · 第 ${row.basis.level} 级`,
      detail: row.basis.level === 5
        ? `${row.basis.model.name} · ${row.basis.model.date}；${row.basis.model.rationale}；采纳依据：${row.basis.model.approval}`
        : row.basis.references.map(ref => `${ref.source}：${ref.locator}`).join('；')
    })).concat(local);
  }
  if (typeof module !== 'undefined') { module.exports = {rowsFor}; return; }
  let generation = 0;
  async function render() {
    const current = ++generation;
    document.getElementById('kb-label-evidence')?.remove();
    if (!['current', 'translated'].includes(root.SKOSMOS?.vocab) || !root.SKOSMOS?.uri) return;
    const uri = root.SKOSMOS.uri;
    const heading = document.querySelector('#concept-preflabel');
    if (!heading) return;
    try {
      const response = await fetch(root.SKOSMOS.vocab === 'translated' ? 'resource/labels-translated/label-provenance.json' : 'resource/labels/label-provenance.json', {cache: 'no-store'});
      if (!response.ok) throw new Error('Label evidence unavailable');
      const rows = rowsFor(await response.json(), uri);
      if (current !== generation || root.SKOSMOS.uri !== uri || !rows.length) return;
      const section = document.createElement('section');
      section.id = 'kb-label-evidence'; section.setAttribute('aria-label', '中文标签依据');
      for (const row of rows) {
        const line = document.createElement('p');
        line.textContent = `${row.label} (${row.language}，${row.kind}) · ${row.notice}`;
        section.appendChild(line);
        const details = document.createElement('details'), summary = document.createElement('summary');
        summary.textContent = '译名依据'; details.appendChild(summary);
        const text = document.createElement('p'); text.textContent = row.detail; details.appendChild(text);
        section.appendChild(details);
      }
      (heading.closest('#concept-heading') || heading.parentElement).after(section);
    } catch (error) {
      if (current !== generation) return;
      const warning = document.createElement('p'); warning.id='kb-label-evidence';
      warning.textContent='中文标签依据暂时不可用，请刷新或重新导入。';
      (heading.closest('#concept-heading') || heading.parentElement).after(warning);
    }
  }
  document.addEventListener('loadConceptPage', render);
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', render);
  else render();
})(typeof window === 'undefined' ? globalThis : window);
