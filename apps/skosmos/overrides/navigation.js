/* Application-only navigation. Does not create or update RDF statements. */
(function (root) {
  const label = (record, lang, uri) => record.labels[lang] || record.labels.en || Object.values(record.labels)[0] || uri;
  function context(nav, scheme, lang) {
    return {nav, scheme, lang, members: new Set(nav.schemes[scheme].members)};
  }
  function concept(ctx, uri, path = []) {
    const record = ctx.nav.nodes[uri];
    const repeated = path.includes(uri);
    return {uri, label: label(record, ctx.lang, uri) + (repeated ? ' ↻' : ''), notation: record.notation,
      children: [], isOpen: false, isScheme: false, navScheme: ctx.scheme, navPath: [...path, uri],
      hasChildren: !repeated && record.children.some(id => ctx.members.has(id))};
  }
  function children(nav, node, lang) {
    const ctx = context(nav, node.isScheme ? node.uri : node.navScheme, lang);
    const scheme = nav.schemes[ctx.scheme];
    const ids = node.isScheme ? [...scheme.entries, ...scheme.unconnected] : nav.nodes[node.uri].children.filter(id => ctx.members.has(id));
    const path = node.isScheme ? [] : node.navPath;
    return ids.map(id => concept(ctx, id, path)).sort((a,b) => a.label.localeCompare(b.label, lang));
  }
  function roots(nav, lang, selected) {
    return Object.entries(nav.schemes).map(([uri, scheme]) => {
      const node = {uri, label: label(scheme, lang, uri), isScheme: true, navScheme: uri, navPath: [],
        hasChildren: scheme.members.length > 0, children: [], isOpen: false,
        navigationNote: (scheme.explicit ? '已声明的顶层概念' : '浏览入口按本体系内关系排列，不代表来源指定顶层') +
          (scheme.unconnected.length ? `；另列 ${scheme.unconnected.length} 个未连接成员` : '')};
      if (uri === selected) {
        node.isOpen = true; node.children = children(nav, node, lang);
      } else if (scheme.members.includes(selected)) {
        // Find one finite in-scheme path for revealing the selected concept.
        // All other polyhierarchical paths remain available through expansion.
        const members = new Set(scheme.members);
        const entries = new Set([...scheme.entries, ...scheme.unconnected]);
        const queue = [[selected]], seen = new Set([selected]);
        let route;
        for (let i = 0; i < queue.length; i++) {
          const path = queue[i], current = path[path.length - 1];
          if (entries.has(current)) { route = [...path].reverse(); break; }
          for (const parent of nav.nodes[current].parents) {
            if (members.has(parent) && !seen.has(parent)) { seen.add(parent); queue.push([...path, parent]); }
          }
        }
        if (route) {
          let cursor = node;
          for (const id of route) {
            cursor.isOpen = true; cursor.children = children(nav, cursor, lang);
            cursor = cursor.children.find(child => child.uri === id);
          }
          cursor.isOpen = cursor.hasChildren;
          if (cursor.hasChildren) cursor.children = children(nav, cursor, lang);
        }
      }
      return node;
    }).sort((a,b) => a.label.localeCompare(b.label, lang));
  }
  const api = {roots, children};
  if (typeof module !== 'undefined') module.exports = api;
  else root.KBNavigation = api;
})(typeof window === 'undefined' ? globalThis : window);
