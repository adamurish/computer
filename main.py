from paapas import create_app
if __name__ == "__main__":
    app = create_app()
    app.env = 'development'
    app.run()
