# GROW extension - Yaml localization

Extension to mark `.yaml` fields for translation given a custom dictionary.

## Prerequisites

At a minimum, you will need the following tools installed:

1. [Git](http://git-scm.com/)
2. [Grow](https://grow.io)

If you do not have Grow, you can install it using:

```
curl https://install.growsdk.org | bash
```

## Import GROW extension

Add the following settings to your podspec.yaml file.

```
extensions:
  preprocessors:
    - extensions.yaml-localization.GrowYamlLocalization

- kind: fields-localization
  autorun: false
  name: localize-fields
  tags:
    - "#here you can add the path of the files to mark for translation as a list."
```

Run the following command in your terminal.

```
grow localize-fields
```
