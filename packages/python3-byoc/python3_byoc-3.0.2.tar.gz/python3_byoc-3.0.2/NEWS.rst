===============
NEWS about byoc
===============

Overview of changes to byoc in reverse chronological order.

3.0.2
=====

  * Rename `Registry.remove` into `Remove.unregister` for
    consistency. `Registry.remove` is deprecated and will be removed in next
    major version (4.x).

  * `Store` API has been enlarged to better match the various use
    cases. `id` can be specified at build time, `external_url` to guide
    sharing (also used to report syntax error locations), `unload`,
    `is_loaded` and `_load_string` to parse content in the supported syntax.

  * `MemoryStack` now accepts an optional `id` parameter so callers can
    define several such stacks with their own unique id.

  * byoc.stacks now provides `get_shared_store` (`Stack.get_shared_store`
    redirects there but will be deprecated in the future).

  * `CmdlineStore.from_cmdline()` is deprecated and replaced by
    `CmdlineStore.update()` which takes a dictionary rather than a list of
    'name=value' strings. Parsing those values is not the job of the store.


3.0.1
=====

  * `FileStore.save_changes() feature (saving modified (dirty) option
    values) has been merged into FileStore.save() which remains the official
    way to save a configuration changes to disk. This finalizes the "lazy
    writing" part of configuration files. `save_changes` was never part of
    the offical API but has been extensively tested in the `byov`
    project. It's now deprecated and will be removed in the next major
    version (4.x).

  * Fix FileStore serialization, if the None section exists it should be
    serialized first (otherwise it gets mixed with the last serialized
    section which can cause duplicated option definitions. This can only
    occur for configuration created in memory.

3.0.0
=====

  * Drop python2 debian packaging.

  * ListOption now accepts a 'separator' argument defaulting to ','.


2.1.0
=====

  * backport PathOption from byov.

  * default value functions now receive a configuration stack
  parameter. This is a API breaking change.
  

2.0.0
=====

  * The new name is byoc (formerly ols-config) acronimizing Build Your Own
    Config.


1.0.2
=====

  * Overrides from the command line now uses an OrderedDict to preserve user
  order.

  * Expose the caught exception when a conversion from unicode fails.


1.0.1
=====

  * Stores are not saved at exit anymore, this is causing more issues than
    requesting users to save them when needed.
 
  * When saving a store, create the missing directories if needed.

  * Errors on duplicate section or option names.

  * Fix edge cases in parsing leading to formatting differences when saving a
    config file.

  * Fix errors on empty or almost empty files.

1.0.0
=====

  * The new name is ols-config (formerly uci-config).


0.1.4
=====

  * Fix a bug where reloading a store didn't clean previous sections which
    could trigger bugs including the noname section being seen *after* named
    sections.

0.1.3
=====

  * Add a CommandLineStore object for use cases where option values can be
    specified as overrides on the command line.

0.1.2
=====

  * Support python3.

  * Fix empty value parsing ('a=') and the related line handling.

0.1.1
=====

  * Add debian packaging (ubuntu native for now).

0.1.0
=====

  * Add MANDATORY as a special default value for options that must be set.

  * Provide support to write cmdline UI.

0.0.3
=====

  * Fix pyflakes issues.

0.0.2
=====

  * Revert to python2 to match current needs.

  * Fix bugs in exceptions messages.

  * Support a default value for RegistryOption.

  * Fix comment handling for config values.

  * Support Store sharing inside the same process.

  * Fix comment handling for sections.

0.0.1
=====

First release.
