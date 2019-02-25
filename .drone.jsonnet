local PythonVersions(pyversion="2.7") = {
    name: "python" + pyversion,
    image: "python:" + pyversion,
    pull: "always",
    environment: {
      PYTHON_LINT: "flake8 flake8-colors pep8-naming",
      PYTHON_TEST: "pytest pytest-cov pytest-mock"
    },
    commands: [
      "pip install --upgrade pip setuptools wheel virtualenv -qq",
      "virtualenv /env-test",
      "env /env-test/bin/pip install $PYTHON_TEST -qq",
      "env /env-test/bin/pip install -e . -qq",
      "env /env-test/bin/pytest --cov=ansibleroler tests/ -v",
      "virtualenv /env-lint",
	  "env /env-lint/bin/pip install $PYTHON_LINT -qq",
	  "env /env-lint/bin/flake8 ansibleroler"
    ],
    depends_on: [
      "clone",
    ],
};

local PipelineTesting = {
  kind: "pipeline",
  name: "testing",
  platform: {
    os: "linux",
    arch: "amd64",
  },
  steps: [
    PythonVersions(pyversion="2.7"),
    PythonVersions(pyversion="3.4"),
    PythonVersions(pyversion="3.5"),
    PythonVersions(pyversion="3.6"),
    PythonVersions(pyversion="3.7"),
  ],
  trigger: {
    branch: [ "master" ],
  },
};

local PipelineBuild = {
  kind: "pipeline",
  name: "build",
  platform: {
    os: "linux",
    arch: "amd64",
  },
  steps: [
    {
      name: "build",
      image: "python:3.7",
      pull: "always",
      commands: [
        "python setup.py sdist bdist_wheel",
      ]
    },
    {
      name: "checksum",
      image: "alpine",
      pull: "always",
      commands: [
        "apk add --no-cache coreutils",
        "sha256sum -b dist/* > sha256sum.txt"
      ],
      when: {
        event: [ "push", "tag" ],
      },
    },
    {
      name: "gpg-sign",
      image: "plugins/gpgsign:1",
      pull: "always",
      settings: {
        key: { "from_secret": "gpgsign_key" },
        passphrase: { "from_secret": "gpgsign_passphrase" },
        detach_sign: true,
        files: [ "dist/*" ],
      },
    },
    {
      name: "publish-github",
      image: "plugins/github-release",
      pull: "always",
      settings: {
        api_key: { "from_secret": "github_token"},
        files: ["dist/*", "sha256sum.txt"],
      },
      when: {
        event: [ "tag" ],
      },
    },
  ],
  depends_on: [
    "testing",
  ],
  trigger: {
    branch: [ "master" ],
  },
};

local PipelineNotifications = {
  kind: "pipeline",
  name: "notifications",
  platform: {
    os: "linux",
    arch: "amd64",
  },
  steps: [
    {
      image: "plugins/matrix",
      settings: {
        homeserver: "https://matrix.rknet.org",
        roomid: "MtidqQXWWAtQcByBhH:rknet.org",
        template: "Status: **{{ build.status }}**<br/> Build: [{{ repo.Owner }}/{{ repo.Name }}]({{ build.link }}) ({{ build.branch }}) by {{ build.author }}<br/> Message: {{ build.message }}",
        username: { "from_secret": "matrix_username" },
        password: { "from_secret": "matrix_password" },
      },
    },
  ],
  depends_on: [
    "build",
  ],
  trigger: {
    branch: [ "master" ],
    event: [ "push", "tag" ],
    status: [ "success", "failure" ],
  },
};

[
  PipelineTesting,
  PipelineBuild,
]
