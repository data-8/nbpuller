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

nbpuller can be activated through a link in the following format:

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

Files at each `<path>` of the given branch will be retrieved using git.

Alternative setting will be:

| Field name    | Required / Default |
|---------------|--------------------|
| file_url      | REQUIRED           |

`<file> should be a url. An example is ?file_url=http://localhost/README.md`

## Expected behavior

If the destination folder is empty, nbpuller will `git clone` remote repo.

If the destination folder exist, in general, nbpuller tries to do `git pull` and merge with `-Xours` parameter, if necessary. In the case that there is any change in the folder, nbpuller will `git add` all of them and commit them, before pulling and merging.

## Cal Blueprint

![bp](https://cloud.githubusercontent.com/assets/2468904/11998649/8a12f970-aa5d-11e5-8dab-7eef0766c793.png "BP Banner")

This project was worked on in close collaboration with
**[Cal Blueprint](http://www.calblueprint.org/)**.
Cal Blueprint is a student-run UC Berkeley organization devoted to matching
the skills of its members to our desire to see
social good enacted in our community. Each semester, teams of 4-5 students work
closely with a non-profit to bring technological solutions to the problems they
face every day.
