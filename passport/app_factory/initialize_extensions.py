def initialize_extensions(app, extensions):
    for extension in extensions:
        extension.init_app(app)
