import tuiargs

# This file shows an example of how an hypothetical git wrapper could be
# implemented:
#
#   1. Create a "menu_structure" dictionary with one key for each possible git
#      operation ("clone", "diff", "commit", etc...)
#
#   2. The value associated to each of those keys is a list of all possible
#      arguments/options/positional values/etc... available for that type of git
#      operation, together with its documentation (directly copied from "man
#      git")
#
#   3. Start the TUI to present all possible options to the user and collect his
#      selection:
#
#          args = tuiargs.Build(menu_structure).run()"
#
#   4. Finally, invoke git with the selected arguments:
#
#          os.system(f"git {' '.join(args)}"
#
# What you will find bellow is an *incomplete* implementation, where:
#
#   * All "git clone" options have been included (as found in "git help clone")
#
#   * Only a few of the options of "git diff" have been included
#
#   * All other git commands are missing.



################################################################################
## Menu layout
################################################################################

menu_structure = \
[
  {
    "type"        : "menu",
    "label"       : "Clone",
    "description" : """\
                    Clones a repository into a newly created directory, creates
                    remote-tracking branches for each branch in the cloned
                    repository (visible using git branch --remotes), and creates
                    and checks out an initial branch that is forked from the
                    cloned repository’s currently active branch.

                    After the clone, a plain git fetch without arguments will
                    update all the remote-tracking branches, and a git pull
                    without arguments will in addition merge the remote master
                    branch into the current master branch, if any (this is
                    untrue when "--single-branch" is given; see below).

                    This default configuration is achieved by creating
                    references to the remote branch heads under
                    refs/remotes/origin and by initializing remote.origin.url
                    and remote.origin.fetch configuration variables.
                    """,
    "trigger"     : "clone",
    "value"       : [
      {
        "type"        : "flag",
        "label"       : "Local",
        "description" : """\
                        When the repository to clone from is on a local machine,
                        this flag bypasses the normal "Git aware" transport
                        mechanism and clones the repository by making a copy of
                        HEAD and everything under objects and refs directories.
                        The files under .git/objects/ directory are hardlinked
                        to save space when possible.

                        If the repository is specified as a local path (e.g.,
                        /path/to/repo), this is the default, and --local is
                        essentially a no-op. If the repository is specified as a
                        URL, then this flag is ignored (and we never use the
                        local optimizations). Specifying --no-local will
                        override the default when /path/to/repo is given, using
                        the regular Git transport instead.

                        If the repository’s $GIT_DIR/objects has symbolic links
                        or is a symbolic link, the clone will fail. This is a
                        security measure to prevent the unintentional copying of
                        files by dereferencing the symbolic links.

                        NOTE: this operation can race with concurrent
                        modification to the source repository, similar to
                        running cp -r src dst while modifying src.
                        """,
        "trigger"     : "--local",
        "value"       : "0/1",
      },
      {
        "type"        : "flag",
        "label"       : "No hard links",
        "description" : """\
                        Force the cloning process from a repository on a local
                        filesystem to copy the files under the .git/objects
                        directory instead of using hardlinks. This may be
                        desirable if you are trying to make a back-up of your
                        repository.
                        """,
        "trigger"     : "--no-hardlinks",
        "value"       : "0/1",
      },
      {
        "type"        : "flag",
        "label"       : "Shared",
        "description" : """\
                        When the repository to clone is on the local machine,
                        instead of using hard links, automatically setup
                        .git/objects/info/alternates to share the objects with
                        the source repository. The resulting repository starts
                        out without any object of its own.

                        NOTE: this is a possibly dangerous operation; do not use
                        it unless you understand what it does. If you clone your
                        repository using this option and then delete branches
                        (or use any other Git command that makes any existing
                        commit unreferenced) in the source repository, some
                        objects may become unreferenced (or dangling). These
                        objects may be removed by normal Git operations (such as
                        git commit) which automatically call git maintenance run
                        --auto. (See git- maintenance(1).) If these objects are
                        removed and were referenced by the cloned repository,
                        then the cloned repository will become corrupt.

                        Note that running git repack without the --local option
                        in a repository cloned with --shared will copy objects
                        from the source repository into a pack in the cloned
                        repository, removing the disk space savings of clone
                        --shared. It is safe, however, to run git gc, which uses
                        the --local option by default.

                        If you want to break the dependency of a repository
                        cloned with --shared on its source repository, you can
                        simply run git repack -a to copy all objects from the
                        source repository into a pack in the cloned repository.
                        """,
        "trigger"     : "--shared",
        "value"       : "0/1",
      },
      {
        "type"        : "option",
        "label"       : "Reference repository",
        "description" : """\
                        If the reference repository is on the local machine,
                        automatically setup .git/objects/info/alternates to
                        obtain objects from the reference repository. Using an
                        already existing repository as an alternate will require
                        fewer objects to be copied from the repository being
                        cloned, reducing network and local storage costs. When
                        using the --reference-if-able, a non existing directory
                        is skipped with a warning instead of aborting the clone.

                        NOTE: see the NOTE for the --shared option, and also the
                        --dissociate option.
                        """,
        "trigger"     : "--reference",
        "value"       : "",
      },
      {
        "type"        : "option",
        "label"       : "Reference repository (if able)",
        "description" : """\
                        Same as "Reference repository" but a non existing
                        directory is skipped with a warning instead of aborting
                        the clone.
                        """,
        "trigger"     : "--reference-if-able",
        "value"       : "",
      },
      {
        "type"        : "flag",
        "label"       : "Dissociate",
        "description" : """\
                        Borrow the objects from reference repositories specified
                        with the --reference options only to reduce network
                        transfer, and stop borrowing from them after a clone is
                        made by making necessary local copies of borrowed
                        objects. This option can also be used when cloning
                        locally from a repository that already borrows objects
                        from another repository—the new repository will borrow
                        objects from the same repository, and this option can be
                        used to stop the borrowing.
                        """,
        "trigger"     : "--dissociate",
        "value"       : "0/1",
      },
      {
        "type"        : "flag",
        "label"       : "Quiet",
        "description" : """\
                        Operate quietly. Progress is not reported to the
                        standard error stream.
                        """,
        "trigger"     : "--quiet",
        "value"       : "0/1",
      },
      {
        "type"        : "flag",
        "label"       : "Verbose",
        "description" : """\
                        Run verbosely. Does not affect the reporting of progress
                        status to the standard error stream.
                        """,
        "trigger"     : "--verbose",
        "value"       : "0/1",
      },
      {
        "type"        : "flag",
        "label"       : "Show progress",
        "description" : """\
                        Progress status is reported on the standard error stream
                        by default when it is attached to a terminal, unless
                        --quiet is specified. This flag forces progress status
                        even if the standard error stream is not directed to a
                        terminal.
                        """,
        "trigger"     : "--progress",
        "value"       : "0/1",
      },
      {
        "type"        : "option",
        "label"       : "Server option",
        "description" : """\
                        Transmit the given string to the server when
                        communicating using protocol version 2. The given string
                        must not contain a NUL or LF character. The server’s
                        handling of server options, including unknown ones, is
                        server-specific. When multiple --server-option=<option>
                        are given, they are all sent to the other side in the
                        order listed on the command line. When no
                        --server-option=<option> is given from the command line,
                        the values of configuration variable
                        remote.<name>.serverOption are used instead.
                        """,
        "trigger"     : "--server-option",
        "value"       : "",
      },
      {
        "type"        : "flag",
        "label"       : "No checkout",
        "description" : """\
                        No checkout of HEAD is performed after the clone is
                        complete.
                        """,
        "trigger"     : "--no-checkout",
        "value"       : "0/1",
      },
      {
        "type"        : "flag",
        "label"       : "Reject shallow",
        "description" : """\
                        Fail if the source repository is a shallow repository.
                        The clone.rejectShallow configuration variable can be
                        used to specify the default.
                        """,
        "trigger"     : "--reject-shallow",
        "value"       : "0/1",
      },
      {
        "type"        : "flag",
        "label"       : "Bare",
        "description" : """\
                        Make a bare Git repository. That is, instead of creating
                        <directory> and placing the administrative files in
                        <directory>/.git, make the <directory> itself the
                        $GIT_DIR. This obviously implies the --no-checkout
                        because there is nowhere to check out the working tree.
                        Also the branch heads at the remote are copied directly
                        to corresponding local branch heads, without mapping
                        them to refs/remotes/origin/. When this option is used,
                        neither remote-tracking branches nor the related
                        configuration variables are created.
                        """,
        "trigger"     : "--bare",
        "value"       : "0/1",
      },
      {
        "type"        : "flag",
        "label"       : "Sparse",
        "description" : """\
                        Employ a sparse-checkout, with only files in the
                        toplevel directory initially being present. The
                        git-sparse-checkout(1) command can be used to grow the
                        working directory as needed.
                        """,
        "trigger"     : "--sparse",
        "value"       : "0/1",
      },
      {
        "type"        : "option",
        "label"       : "Filter",
        "description" : """\
                        Use the partial clone feature and request that the
                        server sends a subset of reachable objects according to
                        a given object filter. When using --filter, the supplied
                        <filter-spec> is used for the partial clone filter. For
                        example, --filter=blob:none will filter out all blobs
                        (file contents) until needed by Git.  Also,
                        --filter=blob:limit=<size> will filter out all blobs of
                        size at least <size>. For more details on filter
                        specifications, see the --filter option in git-
                        rev-list(1).
                        """,
        "trigger"     : "--filter",
        "value"       : "",
      },
      {
        "type"        : "flag",
        "label"       : "Also filter submodules",
        "description" : """\
                        Also apply the partial clone filter to any submodules in
                        the repository. Requires --filter and
                        --recurse-submodules. This can be turned on by default
                        by setting the clone.filterSubmodules config option.
                        """,
        "trigger"     : "--also-filter-submodules",
        "value"       : "0/1",
      },
      {
        "type"        : "option",
        "label"       : "Mirror",
        "description" : """\
                        Set up a mirror of the source repository. This implies
                        --bare. Compared to --bare, --mirror not only maps local
                        branches of the source to local branches of the target,
                        it maps all refs (including remote-tracking branches,
                        notes etc.) and sets up a refspec configuration such
                        that all these refs are overwritten by a git remote
                        update in the target repository.
                        """,
        "trigger"     : "--filter",
        "value"       : "",
      },
      {
        "type"        : "option",
        "label"       : "Origin",
        "description" : """\
                        Instead of using the remote name origin to keep track of
                        the upstream repository, use <name>. Overrides
                        clone.defaultRemoteName from the config.
                        """,
        "trigger"     : "--origin",
        "value"       : "",
      },
      {
        "type"        : "option",
        "label"       : "Branch",
        "description" : """\
                        Instead of pointing the newly created HEAD to the branch
                        pointed to by the cloned repository’s HEAD, point to
                        <name> branch instead. In a non-bare repository, this is
                        the branch that will be checked out.  --branch can also
                        take tags and detaches the HEAD at that commit in the
                        resulting repository.
                        """,
        "trigger"     : "--branch",
        "value"       : "",
      },
      {
        "type"        : "option",
        "label"       : "Revision",
        "description" : """\
                        Create a new repository, and fetch the history leading
                        to the given revision <rev> (and nothing else), without
                        making any remote-tracking branch, and without making
                        any local branch, and detach HEAD to <rev>. The argument
                        can be a ref name (e.g.  refs/heads/main or
                        refs/tags/v1.0) that peels down to a commit, or a
                        hexadecimal object name. This option is incompatible
                        with --branch and --mirror.
                        """,
        "trigger"     : "--revision",
        "value"       : "",
      },
      {
        "type"        : "option",
        "label"       : "Upload pack",
        "description" : """\
                        When given, and the repository to clone from is accessed
                        via ssh, this specifies a non-default path for the
                        command run on the other end.
                        """,
        "trigger"     : "--upload-pack",
        "value"       : "",
      },
      {
        "type"        : "option",
        "label"       : "Template",
        "description" : """\
                        Specify the directory from which templates will be used;
                        (See the "TEMPLATE DIRECTORY" section of git-init(1).)
                        """,
        "trigger"     : "--template",
        "value"       : "",
      },
      {
        "type"        : "option",
        "label"       : "Config",
        "description" : """\
                        Set a configuration variable in the newly-created
                        repository; this takes effect immediately after the
                        repository is initialized, but before the remote history
                        is fetched or any files checked out. The <key> is in the
                        same format as expected by git-config(1) (e.g.,
                        core.eol=true). If multiple values are given for the
                        same key, each value will be written to the config file.
                        This makes it safe, for example, to add additional fetch
                        refspecs to the origin remote.

                        Due to limitations of the current implementation, some
                        configuration variables do not take effect until after
                        the initial fetch and checkout. Configuration variables
                        known to not take effect are: remote.<name>.mirror and
                        remote.<name>.tagOpt. Use the corresponding --mirror and
                        --no-tags options instead.
                        """,
        "trigger"     : "--config",
        "value"       : "",
      },
      {
        "type"        : "option",
        "label"       : "Depth",
        "description" : """\
                        Create a shallow clone with a history truncated to the
                        specified number of commits. Implies --single-branch
                        unless --no-single-branch is given to fetch the
                        histories near the tips of all branches. If you want to
                        clone submodules shallowly, also pass
                        --shallow-submodules.
                        """,
        "trigger"     : "--depth",
        "value"       : "",
      },
      {
        "type"        : "option",
        "label"       : "Shallow since",
        "description" : """\
                        Create a shallow clone with a history, excluding commits
                        reachable from a specified remote branch or tag. This
                        option can be specified multiple times.
                        """,
        "trigger"     : "--shallow-since",
        "value"       : "",
      },
      {
        "type"        : "option",
        "label"       : "Shallow exclude",
        "description" : """\
                        Create a shallow clone with a history, excluding commits
                        reachable from a specified remote branch or tag. This
                        option can be specified multiple times.
                        """,
        "trigger"     : "--shallow-exclude",
        "value"       : "",
      },
      {
        "type"        : "flag",
        "label"       : "Single branch",
        "description" : """\
                        Clone only the history leading to the tip of a single
                        branch, either specified by the --branch option or the
                        primary branch remote’s HEAD points at. Further fetches
                        into the resulting repository will only update the
                        remote-tracking branch for the branch this option was
                        used for the initial cloning. If the HEAD at the remote
                        did not point at any branch when --single-branch clone
                        was made, no remote-tracking branch is created.
                        """,
        "trigger"     : "--single-branch",
        "value"       : "0/1",
      },
      {
        "type"        : "flag",
        "label"       : "Tags",
        "description" : """\
                        Control whether or not tags will be cloned. When
                        --no-tags is given, the option will be become permanent
                        by setting the remote.<remote>.tagOpt=--no-tags
                        configuration. This ensures that future git pull and git
                        fetch won’t follow any tags. Subsequent explicit tag
                        fetches will still work (see git-fetch(1)).

                        By default, tags are cloned and passing --tags is thus
                        typically a no-op, unless it cancels out a previous
                        --no-tags.

                        Can be used in conjunction with --single-branch to clone
                        and maintain a branch with no references other than a
                        single cloned branch. This is useful e.g. to maintain
                        minimal clones of the default branch of some repository
                        for search indexing.
                        """,
        "trigger"     : "--tags",
        "value"       : "0/1",
      },
      {
        "type"        : "flag",
        "label"       : "Recurse submodules",
        "description" : """\
                        After the clone is created, initialize and clone
                        submodules within based on the provided <pathspec>. If
                        no =<pathspec> is provided, all submodules are
                        initialized and cloned. This option can be given
                        multiple times for pathspecs consisting of multiple
                        entries. The resulting clone has submodule.active set to
                        the provided pathspec, or "." (meaning all submodules)
                        if no pathspec is provided.

                        Submodules are initialized and cloned using their
                        default settings. This is equivalent to running git
                        submodule update --init --recursive <pathspec>
                        immediately after the clone is finished. This option is
                        ignored if the cloned repository does not have a
                        worktree/checkout (i.e. if any of --no-checkout/-n,
                        --bare, or --mirror is given)
                        """,
        "trigger"     : "--recurse-submodules",
        "value"       : "0/1",
      },
      {
        "type"        : "flag",
        "label"       : "Shallow submodules",
        "description" : """\
                        All submodules which are cloned will be shallow with a
                        depth of 1.
                        """,
        "trigger"     : "--shallow-submodules",
        "value"       : "0/1",
      },
      {
        "type"        : "flag",
        "label"       : "Remote submodules",
        "description" : """\
                        All submodules which are cloned will use the status of
                        the submodule’s remote-tracking branch to update the
                        submodule, rather than the superproject’s recorded
                        SHA-1. Equivalent to passing --remote to git submodule
                        update.
                        """,
        "trigger"     : "--remote-submodules",
        "value"       : "0/1",
      },
      {
        "type"        : "option",
        "label"       : "Separate git dir",
        "description" : """\
                        Instead of placing the cloned repository where it is
                        supposed to be, place the cloned repository at the
                        specified directory, then make a filesystem-agnostic Git
                        symbolic link to there. The result is Git repository can
                        be separated from working tree.
                        """,
        "trigger"     : "--separate-git-dir",
        "value"       : "",
      },
      {
        "type"        : "option",
        "label"       : "Ref format",
        "description" : """\
                        Specify the given ref storage format for the repository. The valid values are:

                        • files for loose files with packed-refs. This is the
                        default.

                        • reftable for the reftable format. This format is
                        experimental and its internals are subject to change.
                        """,
        "trigger"     : "--ref-format",
        "value"       : "",
      },
      {
        "type"        : "option",
        "label"       : "Jobs",
        "description" : """\
                        The number of submodules fetched at the same time.
                        Defaults to the submodule.fetchJobs option.
                        """,
        "trigger"     : "--jobs",
        "value"       : "",
      },
      {
        "type"        : "option",
        "label"       : "Bundle URI",
        "description" : """\
                        Before fetching from the remote, fetch a bundle from the
                        given <uri> and unbundle the data into the local
                        repository. The refs in the bundle will be stored under
                        the hidden refs/bundle/* namespace. This option is
                        incompatible with --depth, --shallow-since, and
                        --shallow-exclude.
                        """,
        "trigger"     : "--bundle-uri",
        "value"       : "",
      },
      {
        "type"        : "positional argument",
        "label"       : "Repository",
        "description" : """\
                        The (possibly remote) <repository> to clone from. See
                        the GIT URLS section below for more information on
                        specifying repositories.
                        """,
        "trigger"     : "",
        "value"       : "",
      },
      {
        "type"        : "positional argument",
        "label"       : "Directory",
        "description" : """\
                        The name of a new directory to clone into. The
                        "humanish" part of the source repository is used if no
                        <directory> is explicitly given (repo for
                        /path/to/repo.git and foo for host.xz:foo/.git). Cloning
                        into an existing directory is only allowed if the
                        directory is empty.
                        """,
        "trigger"     : "",
        "value"       : "",
      },
      {
        "type"        : "endpoint",
        "label"       : "Run!",
        "description" : "",
        "trigger"     : "",
        "value"       : None,
       },
    ],
  },
  {
    "type"        : "menu",
    "label"       : "Diff",
    "description" : """\
                    Show changes between the working tree and the index or a
                    tree, changes between the index and a tree, changes between
                    two trees, changes resulting from a merge, changes between
                    two blob objects, or changes between two files on disk.
                    """,
    "trigger"     : "diff",
    "value"       : [
      {
        "type"        : "flag",
        "label"       : "Indent heuristic",
        "description" : """\
                        Enable the heuristic that shifts diff hunk boundaries to
                        make patches easier to read.  This is the default.
                        """,
        "trigger"     : "--indent-heuristic",
        "value"       : "0/1",
      },
      {
        "type"        : "option",
        "label"       : "Diff algorithm",
        "description" : """\
                        Choose a diff algorithm. The variants are as follows:

                        myers: The basic greedy diff algorithm.  Currently, this
                        is the default.

                        minimal: Spend extra time to make sure the smallest
                        possible diff is produced.

                        patience: Use "patience diff" algorithm when generating
                        patches.

                        histogram: This algorithm extends the patience algorithm
                        to "support low-occurrence common elements".
                        """,
        "trigger"     : "--diff-algorithm",
        "value"       : "myers",
      },
      {
        "type"        : "flag",
        "label"       : "TO BE IMPLEMENTED",
        "description" : """\
                        Many other options for DIFF are yet to be implemented
                        """,
        "trigger"     : "--to-be-implemented",
        "value"       : "0/1",
      },
      {
        "type"        : "menu",
        "label"       : "Compare workdir to staging area",
        "description" : """\
                        This form is to view the changes you made relative to
                        the index (staging area for the next commit). In other
                        words, the differences are what you could tell Git to
                        further add to the index but you still haven’t. You can
                        stage these changes by using git-add(1).
                        """,
        "trigger"     : "",
        "value"       : [
          {
            "type"        : "positional argument",
            "label"       : "Path",
            "description" : """\
                            (Optional) If specified, the diff will only take the
                            provided path in consideration.
                            """,
            "trigger"     : "--",
            "value"       : "",
          },
          {
            "type"        : "endpoint",
            "label"       : "Run!",
            "description" : "",
            "trigger"     : "",
            "value"       : None,
           },
        ],
      },
      {
        "type"        : "menu",
        "label"       : "Compare staged changes to commit",
        "description" : """\
                        This form is to view the changes you staged for the next
                        commit relative to the named <commit>. Typically you
                        would want comparison with the latest commit, so if you
                        do not give <commit>, it defaults to HEAD. If HEAD does
                        not exist (e.g. unborn branches) and <commit> is not
                        given, it shows all staged changes.  --staged is a
                        synonym of --cached.
                        """,
        "trigger"     : "--cached",
        "value"       : [
          {
            "type"        : "positional argument",
            "label"       : "Commit",
            "description" : """\
                            Commit to compare to.
                            """,
            "trigger"     : "",
            "value"       : "HEAD",
          },
          {
            "type"        : "positional argument",
            "label"       : "Path",
            "description" : """\
                            (Optional) If specified, the diff will only take the
                            provided path in consideration.
                            """,
            "trigger"     : "--",
            "value"       : "",
          },
          {
            "type"        : "endpoint",
            "label"       : "Run!",
            "description" : "",
            "trigger"     : "",
            "value"       : None,
           },
        ],
      },
      {
        "type"        : "menu",
        "label"       : "Compare two folders on the filesystem",
        "description" : """\
                        This form is to compare the given two paths on the
                        filesystem.
                        """,
        "trigger"     : "--no-index",
        "value"       : [
          {
            "type"        : "positional argument",
            "label"       : "Path #1",
            "description" : """\
                            Path to the first folder to compare
                            """,
            "trigger"     : "--",
            "value"       : "",
          },
          {
            "type"        : "positional argument",
            "label"       : "Path #2",
            "description" : """\
                            Path to the second folder to compare
                            """,
            "trigger"     : "",
            "value"       : "",
          },
          {
            "type"        : "endpoint",
            "label"       : "Run!",
            "description" : "",
            "trigger"     : "",
            "value"       : None,
           },
        ],
      },
    ],
  },
  {
    "type"        : "menu",
    "label"       : "Commit",
    "description" : """\
                   Create a new commit containing the current contents of the
                   index and the given log message describing the changes. The
                   new commit is a direct child of HEAD, usually the tip of the
                   current branch, and the branch is updated to point to it
                    """,
    "trigger"     : "commit",
    "value"       : [
      {
        "type"        : "flag",
        "label"       : "TO BE IMPLEMENTED",
        "description" : """\
                        All options for COMMIT are yet to be implemented
                        """,
        "trigger"     : "--to-be-implemented",
        "value"       : "0/1",
      },
      {
        "type"        : "endpoint",
        "label"       : "Run!",
        "description" : "",
        "trigger"     : "",
        "value"       : None,
       },
    ],
  },
  {
    "type"        : "menu",
    "label"       : "Rebase",
    "description" : """\
                    Reapply commits on top of another base tip
                    """,
    "trigger"     : "rebase",
    "value"       : [
      {
        "type"        : "flag",
        "label"       : "TO BE IMPLEMENTED",
        "description" : """\
                        All options for REBASE are yet to be implemented
                        """,
        "trigger"     : "--to-be-implemented",
        "value"       : "0/1",
      },
      {
        "type"        : "endpoint",
        "label"       : "Run!",
        "description" : "",
        "trigger"     : "",
        "value"       : None,
       },
    ],
  },
  {
    "type"        : "menu",
    "label"       : "Other git commands",
    "description" : """\
                    There are many other git commands that are yet to be
                    implemented (branch, merge, init, log, restore, ...)
                    """,
    "trigger"     : "help",
    "value"       : [
      {
        "type"        : "endpoint",
        "label"       : "Run!",
        "description" : "",
        "trigger"     : "",
        "value"       : None,
       },
    ],
  },
]



################################################################################
## Main()
################################################################################

tui  = tuiargs.Build(menu_structure)
args = tui.run()

cmd = f"git {' '.join(args)}"
print(f"Running the following command: {cmd}")

# os.system(cmd) # Uncomment to actually run the command

