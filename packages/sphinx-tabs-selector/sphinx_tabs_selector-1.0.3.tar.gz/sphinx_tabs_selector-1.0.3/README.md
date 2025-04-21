# sphinx_tabs_selector

This plugin is created based on the `sphinx_tabs` plugin and supports all formats supported by `sphinx_tabs`.
In HTML displays, originally, tabs can be switched by clicking. However, this switching functionality is not supported
when generating certain specific formats, such as PDF. This plugin is designed to select the tabs to be displayed and
show them flatly in the generated format. Therefore, it can be used to generate PDF files with selected tabs. Html
format is also supported.

## Installation

```bash
pip install sphinx-tabs-selector
```

## Usage

Add the following configuration to `conf.py`:

```python
extensions = [
    ...
    'sphinx_tabs_selector.selector',
    ...
]

# tabs_include is used to configure the tabs to be selected. Support Unix glob pattern.
# The configuration item is a list. Each element in the list is a string, which is the name of the tab to be selected. 
# If the tab is nested, you need to write down all the names of the tabs in the nesting path.
tabs_include = ["tab1_name", "tab2_name", "tab3_name"]
# tabs_exclude is used to configure the tabs to be skipped. Support Unix glob pattern.
# The configuration item is a list. Each element in the list is a string, which is the name of the tab to be skipped.
tabs_exclude = ["tab4_name", "tab5_name", "tab6_name"]
```

For the way of writing tabs in RST files, you can refer to the documentation of
the [sphinx_tabs](https://sphinx-tabs.readthedocs.io/en/latest/) plugin. Thanks for the author of the sphinx_tabs
plugin.

## Notes

1. If you want to use this plugin. You must add the `tabs_include` or `tabs_exclude` configuration to `conf.py`;
   Otherwise, the plugin will not take effect. Therefore, you can use the `tabs_include` or `tabs_exclude`configuration
   to control the activation of the plugin. If any of the `tabs_include` or `tabs_exclude` configuration is added, the
   plugin will be activated. If either of the `tabs_include` or `tabs_exclude` configuration is not added, the plugin
   will not be activated.
2. If only `tabs_include` is added, the plugin will only select the tabs in the `tabs_include` configuration.
3. If only `tabs_exclude` is added, the plugin will select all tabs except the tabs in the `tabs_exclude` configuration.
4. If both `tabs_include` and `tabs_exclude` are added, the plugin will select the tabs in the `tabs_include`
   configuration, and exclude the tabs in the `tabs_exclude` configuration. **But excluding takes precedence over
   selecting**.
2. If both the `sphinx_tabs` plugin and the `sphinx_tabs_selector` plugin are added to the `extensions` in `conf.py`,
   for the `sphinx_tabs_selector` plugin to work, it must be added after `sphinx_tabs`.
3. The `sphinx_tabs_selector` plugin can be used independently even if the `sphinx_tabs` plugin is not added to
   `conf.py`. 