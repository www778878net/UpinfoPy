from invoke import task, run

@task
def setup(c):
    run("pip install build")
    run("python -m build")
    run("pip install .")

@task
def publish(c):
    c.run("python -m build")
    c.run("twine upload --repository pypi dist/*")

@task
def run_all(c):
    setup(c)
    run("pytest")
    publish(c)

if __name__ == "__main__":
    run_all()