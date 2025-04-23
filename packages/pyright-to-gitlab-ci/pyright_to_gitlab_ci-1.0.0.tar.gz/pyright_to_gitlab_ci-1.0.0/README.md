# pyright-to-gitlab-ci

This is a port of [the NPM package of the same name](https://gitlab.com/ErezAmihud/pyright-to-gitlab-ci)
since [Robert Craigie](https://github.com/RobertCraigie/pyright-python)
(blessed be thy name) took on themself the hard task of actually giving us access
to pyright without having to directly touch any icky NPM setup.

## Using as part of the GitLab CI
I prefer to use UV because I find it easier to scale over time and multiple repos,
but using pip works perfectly

### With UV

`.gitlab-ci.yml`

```yaml
job_name:
  script:
   - uvx pyright <python source> --outputjson > obj/pyright.json
   - uvx pyright-to-gitlab-ci --src obj/pyright.json --output obj/pyright-cc.json --base_path .
  artifacts:
    reports:
      codequality: obj/pyright-cc.json
```

### With pip

`.gitlab-ci.yml`

```yaml
job_name:
  before_script:
  script:
   - pipx pyright <python source> --outputjson > obj/pyright.json
   - pipx pyright-to-gitlab-ci --src obj/pyright.json --output obj/pyright-cc.json --base_path .
  artifacts:
    reports:
      codequality: obj/pyright-cc.json
```

# Changelog

## v1.0.0

- Support extended Python>=3.10
- Fix fingerprinting
- Multiple parsing issues fix
- Added unit tests, with tox for all supported python versions
- pyright passes with no warning
