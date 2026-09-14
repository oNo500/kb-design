"""An explicit source withdrawal permits only one exact set of concept removals."""
import hashlib
import json


def concept_digest(uris):
    return hashlib.sha256(json.dumps(sorted(uris),separators=(',',':')).encode()).hexdigest()


def validate_removal(difference,authorization,active_sources):
    removed=difference['concepts']['removed']
    if not removed:return
    fields={'source','source_sha256','baseline_sha256','concepts_sha256','reason'}
    if (not isinstance(authorization,dict) or set(authorization)!=fields
        or not all(isinstance(v,str) and v.strip() for v in authorization.values())
        or authorization['source'] in active_sources
        or authorization['baseline_sha256']!=(difference.get('baseline') or {}).get('sha256')
        or authorization['concepts_sha256']!=concept_digest(removed)):
        raise ValueError('Cross-version identity loss is not covered by the exact source removal authorization')
    difference['authorized_source_removal']=authorization


def validate_maintenance_removal(difference,config,effects):
    removed=set(difference['concepts']['removed'])
    if not removed:return
    context=config.get('maintenance',{})
    allowed=set(effects.get('deleted_nodes',[]))
    allowed.update(effects.get('selection_excluded_concepts',[]))
    if context:
        if context.get('baseline_sha256')!=(difference.get('baseline') or {}).get('sha256'):
            raise ValueError('Maintenance identity loss baseline differs')
        allowed.update(context.get('removed_source_concepts',[]))
        allowed.update(context.get('removed_local_nodes',[]))
    if removed<=allowed:
        difference['authorized_maintenance_removals']=sorted(removed)
        return
    validate_removal(difference,config.get('source_removal'),config['sources'])
