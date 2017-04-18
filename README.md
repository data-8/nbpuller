# nbpuller
An extension for jupyter notebook to retrieve and update local files from remote git repository using native git pull and merge.

## Installation

You can currently install this directly from git:

```
pip install git+https://github.com/data-8/nbpuller.git
jupyter serverextension enable --py nbpuller
jupyter nbextension install --py nbpuller
```

To enable this extension for all notebooks:

```
jupyter nbextension enable --py nbpuller
```

## Usage

nbpuller can be activated through a HTTP GET request to a link in the following format:

```
<notebook_url>/interact?<settings>
```

`<settings>` has the form of URL query strings, with the following possible parameters:

| Field name    | Required / Default |
|---------------|--------------------|
| domain        | "github.com"       |
| account       | "data-8"           |
| repo          | REQUIRED           |
| branch        | "gh-pages"         |
| path          | REQUIRED, can be multiple |
| notebook_path | ""                 |

The remote git repo url is constructed as follows:
`https://<domain>/<account>/<repo>.git`

Files or directories at each `<path>` of the given branch will be retrieved using git.

For example, `path=README.md` will retrieve a typical README file, while `path=labs/` would retrieve a directory called `labs` in the root of the git repo.

Alternative setting will be:

| Field name    | Required / Default |
|---------------|--------------------|
| file_url      | REQUIRED           |

`file_url` should be a url. An example is `?file_url=http://localhost/README.md`


## Configuration

Nbpuller enforces several whitelists for security.

1. File type whitelist for pulling from arbitary url (using `file_url` option). By default, only `ipynb` file type is allowed. It can be overriden by `ALLOWED_FULETYPES` environment variable, delimited by ":".

2. Domain whitelist for pulling from arbitary url. By default none is allowed. Overriden by `ALLOWED_URL_DOMAIN` variable.

3. Github account whitelist, enforced when pulling from a repo on github. By default, only `data-8` is allowed as an account to pull from. This can be overriden by setting `ALLOWED_GITHUB_ACCOUNTS` variable.

4. Git remote domain whitelist, restricting which domain can the git repo be at. By default, only Github is allowed. This can be overriden by setting `ALLOWED_WEB_DOMAINS` variable.


## Expected behavior

If the destination folder is empty, nbpuller will `git clone` remote repo.

If the destination folder exist, in general, nbpuller tries to do `git pull` and merge with `-Xours` parameter, if necessary. In the case that there is any change in the folder, nbpuller will `git add` all of them and commit them, before pulling and merging.

After files are ready, user will receive a HTTP redirect to the file tree at the last `path` downloaded. In case error, the user will stay at the initial page and see an error output.

## Cal Blueprint

![bp](https://cloud.githubusercontent.com/assets/2468904/11998649/8a12f970-aa5d-11e5-8dab-7eef0766c793.png "BP Banner")

This project was worked on in close collaboration with
**[Cal Blueprint](http://www.calblueprint.org/)**.
Cal Blueprint is a student-run UC Berkeley organization devoted to matching the skills of its members to our desire to see social good enacted in our community. Each semester, teams of 4-5 students work closely with a non-profit to bring technological solutions to the problems they face every day.
