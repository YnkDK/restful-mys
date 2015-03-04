import restful_mys.core as mys
from controller.hello_world import HelloWorld as HelloWorldController
from model.hello_world import HelloWorld as HelloWorldModel

cfg = {
    'DEBUG': True,
}

core = mys.Core(config=cfg)
core.add_resource(HelloWorldController, HelloWorldModel, '/')

core.run()