import invoke


@invoke.task
def pin_requirements(c):
    c.run("pip install pipreqs pip-tools")
    c.run("rm reqs.in reqs.txt || echo nothing-to-delete")
    c.run("pipreqs --savepath reqs.in .")
    c.run("pip-compile --verbose --output-file reqs.txt reqs.in")
