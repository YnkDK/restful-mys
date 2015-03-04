import restful_mys.core as core
from controller.hello_world import HelloWorld as HelloWorldController
from model.hello_world import HelloWorld as HelloWorldModel

cfg = {
    'DEBUG': True,
}

api = core.Core(config=cfg)
api.add_resource(HelloWorldController, HelloWorldModel, '/')

api.run()