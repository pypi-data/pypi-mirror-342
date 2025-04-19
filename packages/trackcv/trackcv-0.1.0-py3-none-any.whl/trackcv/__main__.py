def main():
    # this is a separate function so it can be called from pyproject.toml:project.scripts
    from .main import app

    app()


if __name__ == '__main__':
    main()
