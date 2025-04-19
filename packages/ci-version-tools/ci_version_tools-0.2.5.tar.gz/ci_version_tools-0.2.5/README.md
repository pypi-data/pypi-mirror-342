# Versioning tools for CI

## project-version

Provides version environment variables to CI builds.

<details>
<summary>Example output</summary>

```
$ git tag
v0.1.3
v0.1.4
v0.2.0
v0.3.0

$ cat VERSION
0.3.0

$ project-version --version-source file --version-source-file VERSION env-vars
VERSION_SEMVER=0.3.0
VERSION_MAJOR=0
VERSION_MINOR=3
VERSION_PATCH=0
VERSION_MAJOR_MINOR=0.3
VERSION_WITHOUT_BUILD_METADATA=0.3.0
VERSION_IS_RELEASE=1
VERSION_IS_LATEST_RELEASE=1

$ git checkout v0.1.4

$ cat VERSION
0.1.4

$ project-version --version-source file --version-source-file VERSION env-vars
VERSION_SEMVER=0.1.4
VERSION_MAJOR=0
VERSION_MINOR=1
VERSION_PATCH=4
VERSION_MAJOR_MINOR=0.1
VERSION_WITHOUT_BUILD_METADATA=0.1.4
VERSION_IS_RELEASE=1

$ project-version --version-source file --version-source-file VERSION --git-tag v0.1.3 env-vars
ERROR:ci_version_tools.project:Project version 0.1.5 in does not match the version 0.1.3 in the Git tag.

$ echo 0.3.0 >VERSION

$ project-version --version-source file --version-source-file VERSION env-vars
ERROR:ci_version_tools.project:Version 0.3.0 has been released on a different commit already. Increment the version to a next pre-release to fix this error.

$ echo 0.2.0-rc.1 >VERSION

$ project-version --version-source file --version-source-file VERSION env-vars
ERROR:ci_version_tools.project:Version 0.2.0-rc.1 targets 0.2.0 which has been released already. Increment the version to fix this error.

$ echo 0.4.0-rc.1+deadbeef >VERSION

$ project-version --version-source file --version-source-file VERSION env-vars
VERSION_SEMVER=0.4.0-rc.1+deadbeef
VERSION_MAJOR=0
VERSION_MINOR=4
VERSION_PATCH=0
VERSION_MAJOR_MINOR=0.4
VERSION_WITHOUT_BUILD_METADATA=0.4.0-rc.1
VERSION_PRE_RELEASE=rc.1
VERSION_IS_PRE_RELEASE=1
VERSION_BUILD_METADATA=deadbeef

$ echo 0.4.0 >VERSION

$ project-version --version-source file --version-source-file VERSION --git-tag v0.4.0 env-vars
ERROR:ci_version_tools.project:Release tag v0.4.0 does not exist in git.
```

</details>

Example application in `.gitlab-ci.yml`:

```yaml
version:
  image: docker.io/alikov/ci-version-tools:0.2.0
  stage: .pre
  variables:
    GIT_DEPTH: 0
  script:
    - project-version
        --version-source-file ./VERSION
        --git-version-tag-prefix v
        ${CI_COMMIT_TAG:+--git-tag "$CI_COMMIT_TAG"}
        env-vars | tee version.env
  artifacts:
    reports:
      dotenv: version.env

.build-image:
  stage: build
  image: $BUILDAH_CI_IMAGE
  script:
    - IMAGE="${CI_REGISTRY_IMAGE}:${VERSION_WITHOUT_BUILD_METADATA}"
    - buildah build -t "$IMAGE" .
    - buildah push "$IMAGE"
    - if [ -n "${VERSION_IS_RELEASE:-}" ]; then
        buildah push "$IMAGE" "${CI_REGISTRY_IMAGE}:${VERSION_MAJOR}";
        buildah push "$IMAGE" "${CI_REGISTRY_IMAGE}:${VERSION_MAJOR_MINOR}";
      fi
    - if [ -n "${VERSION_IS_LATEST_RELEASE:-}" ]; then
        buildah push "$IMAGE" "${CI_REGISTRY_IMAGE}:latest";
      fi
  needs:
    - version

```

## version-env-vars

Parses environment variables containing semantic versions into major/minor variants.

<details>
<summary>Example output</summary>

```
$ export ALPINE_VERSION=3.20.2
$ export TERRAFORM_VERSION=1.9.3
$ version-env-vars parse ALPINE_VERSION TERRAFORM_VERSION
ALPINE_VERSION_SEMVER=3.20.2
ALPINE_VERSION_MAJOR=3
ALPINE_VERSION_MINOR=20
ALPINE_VERSION_PATCH=2
ALPINE_VERSION_MAJOR_MINOR=3.20
ALPINE_VERSION_WITHOUT_BUILD_METADATA=3.20.2
ALPINE_VERSION_IS_RELEASE=1
TERRAFORM_VERSION_SEMVER=1.9.3
TERRAFORM_VERSION_MAJOR=1
TERRAFORM_VERSION_MINOR=9
TERRAFORM_VERSION_PATCH=3
TERRAFORM_VERSION_MAJOR_MINOR=1.9
TERRAFORM_VERSION_WITHOUT_BUILD_METADATA=1.9.3
TERRAFORM_VERSION_IS_RELEASE=1
```

</details>

Example application in `.gitlab-cy.yml`:

```yaml
variables:
  ALPINE_VERSION: "3.20.2"
  TERRAFORM_VERSION: "1.9.3"

# https://support.gitlab.com/hc/en-us/articles/18085676898588-Dotenv-variables-exceed-default-limit-in-GitLab-pipelinestool-versions:
  image: docker.io/alikov/ci-version-tools:0.2.0
  stage: .pre
  parallel:
    matrix:
      - VAR_NAME: ALPINE_VERSION
      - VAR_NAME: TERRAFORM_VERSION
  script:
    - version-env-vars parse ALPINE_VERSION TERRAFORM_VERSION | tee "${VAR_NAME}.env"
  artifacts:
    reports:
      dotenv: "${VAR_NAME}.env"

.build-image:
  stage: build
  image: $BUILDAH_CI_IMAGE
  script:
    - IMAGE="${CI_REGISTRY_IMAGE}:${VERSION_WITHOUT_BUILD_METADATA}"
    - buildah build
        --build-arg "BASE_IMAGE=alpine:${ALPINE_VERSION}"
        --build-arg "DOWNLOAD_TERRAFORM_VERSION=${TERRAFORM_VERSION}"
        -t "$IMAGE"
        .
    - buildah inspect "$IMAGE"
    - buildah push "$IMAGE"
    - if [ -n "${VERSION_IS_RELEASE:-}" ]; then
        buildah push "$IMAGE" "${CI_REGISTRY_IMAGE}:alpine-${ALPINE_VERSION_MAJOR_MINOR}";
        buildah push "$IMAGE" "${CI_REGISTRY_IMAGE}:terraform-${TERRAFORM_VERSION_MAJOR_MINOR}";
      fi
  needs:
    - version
    - tool-versions

```

## Developing

See [DEVELOPING.md](DEVELOPING.md) for local development setup instructions.
