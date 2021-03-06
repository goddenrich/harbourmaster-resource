class Source:
    @staticmethod
    def _get_source_value_from_payload(value, payload):
        try:
            return payload['source'][value]
        except KeyError:
            raise KeyError(f'{value} not found')

    def __init__(self, payload):
        self.conduit_uri = self._get_source_value_from_payload('conduit_uri', payload)
        self.conduit_token = self._get_source_value_from_payload('conduit_token', payload)
        self.buildStepPHID = self._get_source_value_from_payload('buildStepPHID', payload)

def get_version_from_payload(payload):
    version = payload.get('version', {}) or {}
    target_id = version.get('target')
    target_phid = version.get('targetPHID')
    diff_id = version.get('diff')
    branch = version.get('branch')
    base = version.get('base')
    return Version(target_id, target_phid, diff_id, branch, base)

class Version:
    def __init__(self, target_id, target_phid, diff_id, branch, base):
        self.target = str(target_id) if target_id else None
        self.targetPHID = str(target_phid) if target_phid else None
        self.diff = str(diff_id) if diff_id else None
        self.branch = str(branch) if branch else None
        self.base = str(base) if base else None

    def dict(self):
        return self.__dict__

def versions_to_json(versions):
    return [version.dict() for version in versions]

class Diff:
    def __init__(self, data):
        self.id = data.get('id')
        
        def get_base(refs):
            for ref in refs:
                if ref.get('type') == "base":
                    return ref.get('identifier')
        def get_branch(refs):
            for ref in refs:
                if ref.get('type') == "branch":
                    return ref.get('name')

        refs = data.get('fields', {}).get('refs', [])
        self.branch = get_branch(refs)
        self.base = get_base(refs)

class Target:
    def __init__(self, data):
        self.id = data.get('id')
        self.phid = data.get('phid')
        self.buildPHID = data.get('fields', {}).get('buildPHID')
        self.status = data.get('fields', {}).get('status')
        self.buildStepPHID = data.get('fields', {}).get('buildStepPHID')

class Build:
    def __init__(self, data):
        self.id = data.get('id')
        self.phid = data.get('phid')
        self.buildablePHID = data.get('fields', {}).get('buildablePHID')

class Buildable:
    def __init__(self, data):
        self.id = data.get('id')
        self.phid = data.get('phid')
        self.objectPHID = data.get('fields', {}).get('objectPHID')
        self.containerPHID = data.get('fields', {}).get('containerPHID')
