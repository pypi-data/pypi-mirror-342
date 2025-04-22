from swarm.core.blueprint_base import BlueprintBase

class DummyBlueprint(BlueprintBase):
    def run(self, messages, **kwargs):
        yield {}

def test_init():
    bp = DummyBlueprint('dummy', config={'foo': 'bar'}, config_path=None)
    assert bp.blueprint_id == 'dummy'
    assert bp._config['foo'] == 'bar'
    print('BlueprintBase init test passed')

if __name__ == '__main__':
    test_init()
